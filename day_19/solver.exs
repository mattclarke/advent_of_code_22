file = "input.txt"

recipes =
  File.stream!(file)
  |> Enum.map(&String.replace(&1, "\n", ""))
  |> Stream.map(&String.split(&1, " "))
  |> Stream.map(&List.to_tuple/1)
  |> Enum.map(fn x ->
    %{
      ore: {String.to_integer(elem(x, 6)), 0, 0},
      clay: {String.to_integer(elem(x, 12)), 0, 0},
      obsidian: {String.to_integer(elem(x, 18)), String.to_integer(elem(x, 21)), 0},
      geode: {String.to_integer(elem(x, 27)), 0, String.to_integer(elem(x, 30))}
    }
  end)
  |> IO.inspect()

defmodule Foo do
  def solve(recipes, rounds) do
    robots = {1, 0, 0, 0}
    Enum.reduce(recipes, [], fn x, acc ->
      {result, _} = run_recipe(x, robots, {0, 0, 0, 0}, rounds, %{})
      [result | acc] end)
    |> Enum.reverse()
  end

  defp run_recipe(_, _, {_, _, _, geode}, 0, cache) do
    {geode, cache}
  end

  defp run_recipe(recipe, robots, materials, rounds, cache) do
    # IO.inspect({rounds, robots, materials})
    cache_value = Map.get(cache, generate_cache_key(robots, materials, rounds))
    # Ugly if use 'when' in signiture?
    if cache_value == nil do
      result = 0

      {result, cache} =
      if can_build("geode", materials, recipe) do
        {r, cache} = applesauce("geode", robots, materials, recipe, rounds, cache)
        {max(result, r), cache}
      else
        {result, cache}
      end

      {result, cache} =
      if can_build("obsidian", materials, recipe) do
        {r, cache} = applesauce("obsidian", robots, materials, recipe, rounds, cache)
        {max(result, r), cache}
      else
        {result, cache}
      end

      {result, cache} =
      if can_build("clay", materials, recipe) do
        {r, cache} = applesauce("clay", robots, materials, recipe, rounds, cache)
        {max(result, r), cache}
      else
        {result, cache}
      end

      {result, cache} =
      if can_build("ore", materials, recipe) do
        {r, cache} = applesauce("ore", robots, materials, recipe, rounds, cache)
        {max(result, r), cache}
      else
        {result, cache}
      end

      {r, cache} = run_recipe(recipe, robots, mine(robots, materials), rounds - 1, cache)
      result = max(result, r)

      cache = Map.put(cache, generate_cache_key(robots, materials, rounds), result)

      {result, cache}
    else
      {cache_value, cache}
    end
  end

  defp applesauce(type, robots, materials, recipe, rounds, cache) do
      materials = mine(robots, materials)
      {robots, materials} = build(type, robots, materials, recipe)
      run_recipe(recipe, robots, materials, rounds - 1, cache)
  end

  defp generate_cache_key(robots, materials, rounds) do
    {robots, materials, rounds}
  end

  defp can_build(type, materials, recipe) do
    recipe =
      case type do
        "ore" ->
          recipe.ore

        "clay" ->
          recipe.clay

        "obsidian" ->
          recipe.obsidian

        "geode" ->
          recipe.geode
      end

    Enum.zip(Tuple.to_list(materials), Tuple.to_list(recipe))
    |> Enum.reduce(true, fn {m, r}, acc ->
      if acc == false do
        false
      else
        if m >= r do
          true
        else
          false
        end
      end
    end)
  end

  defp mine(robots, materials) do
    {rore, rclay, robsidian, rgeode} = robots
    {ore, clay, obsidian, geode} = materials
    {ore + rore, clay + rclay, obsidian + robsidian, geode + rgeode}
  end

  defp build(type, robots, materials, recipe) do
    {rore, rclay, robsidian, rgeode} = robots
    {ore, clay, obsidian, geode} = materials

    case type do
      "ore" ->
        recipe = recipe.ore
        robots = {rore + 1, rclay, robsidian, rgeode}

        materials =
          {ore - elem(recipe, 0), clay - elem(recipe, 1), obsidian - elem(recipe, 2), geode}

        {robots, materials}

      "clay" ->
        recipe = recipe.clay
        robots = {rore, rclay + 1, robsidian, rgeode}

        materials =
          {ore - elem(recipe, 0), clay - elem(recipe, 1), obsidian - elem(recipe, 2), geode}

        {robots, materials}

      "obsidian" ->
        recipe = recipe.obsidian
        robots = {rore, rclay, robsidian + 1, rgeode}

        materials =
          {ore - elem(recipe, 0), clay - elem(recipe, 1), obsidian - elem(recipe, 2), geode}

        {robots, materials}

      "geode" ->
        recipe = recipe.geode
        robots = {rore, rclay, robsidian, rgeode + 1}

        materials =
          {ore - elem(recipe, 0), clay - elem(recipe, 1), obsidian - elem(recipe, 2), geode}

        {robots, materials}
    end
  end
end

result =
  Foo.solve(recipes, 24)
  |> IO.inspect()
  |> Enum.with_index(1)
  |> Enum.reduce(0, fn {v, i}, acc ->
    acc + v * i
  end)
IO.inspect(result)

# IO.puts("Answer to part 1 = #{result}")
