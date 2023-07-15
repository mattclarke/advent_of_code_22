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

defmodule Foo do
  def solve(recipes, rounds) do
    robots = {1, 0, 0, 0}

    Enum.reduce(recipes, [], fn x, acc ->
      {result, _, _} = run_recipe(x, robots, {0, 0, 0, 0}, rounds, %{}, 0, true, true, true)
      [result | acc]
    end)
    |> Enum.reverse()
  end

  defp run_recipe(_, {_, _, _, rgeode}, {_, _, _, geode}, 1, cache, max_geodes, _, _, _) do
    {geode + rgeode, cache, max(max_geodes, geode + rgeode)}
  end

  defp run_recipe(recipe, robots, materials, rounds, cache, max_geodes, can_build_ore, can_build_clay, can_build_obsidian) do
    # IO.inspect({rounds, robots, materials})
    materials = normalise_materials(materials, robots, recipe)
    cache_value = Map.get(cache, generate_cache_key(robots, materials, rounds))
    # Ugly if use 'when' in signiture?
    if cache_value == nil do
      max_possible = calculate_max_possible(materials, robots, rounds)

      if max_possible <= max_geodes do
        # Cannnot possibly get more so don't go any further
        {0, cache, max_geodes}
      else
        result = 0

        {result, cache, max_geodes} =
          if can_build("geode", robots, materials, recipe) do
            {r, cache, max_geodes} =
              applesauce("geode", robots, materials, recipe, rounds, cache, max_geodes, true, true, true)

            {max(result, r), cache, max_geodes}
          else
            {result, cache, max_geodes}
          end

        {result, cache, max_geodes, new_can_build_obsidian} =
          if can_build("obsidian", robots, materials, recipe) and can_build_obsidian do
            {r, cache, max_geodes} =
              applesauce("obsidian", robots, materials, recipe, rounds, cache, max_geodes, true, true, true)

            {max(result, r), cache, max_geodes, false}
          else
            {result, cache, max_geodes, true}
          end

        {result, cache, max_geodes, new_can_build_clay} =
          if can_build("clay", robots, materials, recipe) and can_build_clay do
            {r, cache, max_geodes} =
              applesauce("clay", robots, materials, recipe, rounds, cache, max_geodes, true, true, true)

            {max(result, r), cache, max_geodes, false}
          else
            {result, cache, max_geodes, true}
          end

        {result, cache, max_geodes, new_can_build_ore} =
          if can_build("ore", robots, materials, recipe) and can_build_ore do
            {r, cache, max_geodes} =
              applesauce("ore", robots, materials, recipe, rounds, cache, max_geodes, true, true, true)

            {max(result, r), cache, max_geodes, false}
          else
            {result, cache, max_geodes, true}
          end

        {r, cache, max_geodes} =
          run_recipe(recipe, robots, mine(robots, materials), rounds - 1, cache, max_geodes, new_can_build_ore, new_can_build_clay, new_can_build_obsidian)

        result = max(result, r)

        materials = normalise_materials(materials, robots, recipe)

        key = generate_cache_key(robots, materials, rounds)
        cache =
          Map.put(cache, key, result)

        {result, cache, max_geodes}
      end
    else
      {cache_value, cache, max_geodes}
    end
  end

  defp calculate_max_possible(materials, robots, rounds) do
    {_, _, _, geodes} = materials
    {_, _, _, rgeode} = robots
    # so far + geodes produced by current + geodes produced if one robot created per remaining round
    geodes + rgeode * rounds + rounds * (rounds - 1) / 2
  end

  defp normalise_materials(materials, robots, recipe) do
    {max_ore, max_clay, max_obsidian} =
      Enum.reduce(Map.values(recipe), {0, 0, 0}, fn {o, c, ob}, {mo, mc, mob} ->
        {max(mo, o), max(mc, c), max(mob, ob)}
      end)

    {ore, clay, obsidian, geode} = materials
    {rore, rclay, robsidian, _} = robots

    ore =
      if rore == max_ore and ore > max_ore do
        max_ore
      else
        ore
      end

    clay =
      if rclay == max_clay and clay > max_clay do
        max_clay
      else
        clay
      end

    obsidian =
      if robsidian == max_obsidian and obsidian > max_obsidian do
        max_obsidian
      else
        obsidian
      end

    {ore, clay, obsidian, geode}
  end

  defp applesauce(type, robots, materials, recipe, rounds, cache, max_geodes, can_build_ore, can_build_clay, can_build_obsidian) do
    materials = mine(robots, materials)
    {robots, materials} = build(type, robots, materials, recipe)
    run_recipe(recipe, robots, materials, rounds - 1, cache, max_geodes, can_build_ore, can_build_clay, can_build_obsidian)
  end

  defp generate_cache_key(robots, materials, rounds) do
    {robots, materials, rounds}
  end

  defp can_build(type, robots, materials, recipe) do
    {rore, rclay, robsidian, _} = robots

    {recipe, below_limit} =
      case type do
        "ore" ->
          max_ore =
            Enum.reduce(Map.values(recipe), 0, fn {o, _, _}, acc ->
              max(acc, o)
            end)

          {recipe.ore, rore < max_ore}

        "clay" ->
          max_clay =
            Enum.reduce(Map.values(recipe), 0, fn {_, o, _}, acc ->
              max(acc, o)
            end)

          {recipe.clay, rclay < max_clay}

        "obsidian" ->
          max_obsidian =
            Enum.reduce(Map.values(recipe), 0, fn {_, _, o}, acc ->
              max(acc, o)
            end)

          {recipe.obsidian, robsidian < max_obsidian}

        "geode" ->
          {recipe.geode, true}
      end

    if below_limit do
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
    else
      false
    end
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
  |> Enum.with_index(1)
  |> Enum.reduce(0, fn {v, i}, acc ->
    acc + v * i
  end)

IO.puts("Answer to part 1 = #{result}")

result =
  recipes
  |> Enum.take(3)
  |> Foo.solve(32)
  |> Enum.product()

IO.puts("Answer to part 2 = #{result}")
