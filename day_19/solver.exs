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
    state = create_initial_state()

    Enum.reduce(recipes, [], fn x, acc ->
      {result, _cache, _} =
        run_recipe(x, state, rounds, %{contents: %{}, misses: 0, hits: 0}, 0, true, true, true)

      # IO.puts("cache size: #{map_size(_cache.contents)}")
      # IO.puts("hit percentage: #{100 * cache.hits / (cache.hits + cache.misses)}")
      [result | acc]
    end)
    |> Enum.reverse()
  end

  defp create_initial_state() do
    %{
      robots: {1, 0, 0, 0},
      materials: {0, 0, 0, 0},
      cache: %{}
    }
  end

  defp run_recipe(_, state, 1, cache, max_geodes, _, _, _) do
    {_, _, _, geode} = state.materials
    {_, _, _, rgeode} = state.robots
    {geode + rgeode, cache, max(max_geodes, geode + rgeode)}
  end

  # TODO: try storing the minute in the cache rather than the geodes and then abandon a branch if we
  # hit it later than the cached version.

  defp run_recipe(
         recipe,
         state,
         rounds,
         cache,
         max_geodes,
         can_build_ore,
         can_build_clay,
         can_build_obsidian
       ) do
    state = normalise_materials(state, recipe)
    cache_value = Map.get(cache.contents, generate_cache_key(state, rounds))

    case cache_value do
      nil ->
        cache = %{cache | misses: cache.misses + 1}

        explore_branch(
          recipe,
          state,
          rounds,
          cache,
          max_geodes,
          can_build_ore,
          can_build_clay,
          can_build_obsidian
        )

      value ->
        cache = %{cache | hits: cache.hits + 1}
        {value, cache, max_geodes}
    end
  end

  defp explore_branch(
         recipe,
         state,
         rounds,
         cache,
         max_geodes,
         can_build_ore,
         can_build_clay,
         can_build_obsidian
       ) do
    max_possible = calculate_max_possible(state, rounds)

    if max_possible <= max_geodes do
      # Cannnot possibly get more so don't go any further
      {0, cache, max_geodes}
    else
      result = 0

      {result, cache, max_geodes, _} =
        try_to_build("geode", state, cache, rounds, recipe, true, max_geodes, result)

      {result, cache, max_geodes, new_can_build_obsidian} =
        try_to_build(
          "obsidian",
          state,
          cache,
          rounds,
          recipe,
          can_build_obsidian,
          max_geodes,
          result
        )

      {result, cache, max_geodes, new_can_build_clay} =
        try_to_build("clay", state, cache, rounds, recipe, can_build_clay, max_geodes, result)

      {result, cache, max_geodes, new_can_build_ore} =
        try_to_build("ore", state, cache, rounds, recipe, can_build_ore, max_geodes, result)

      {r, cache, max_geodes} =
        run_recipe(
          recipe,
          mine(state),
          rounds - 1,
          cache,
          max_geodes,
          new_can_build_ore,
          new_can_build_clay,
          new_can_build_obsidian
        )

      result = max(result, r)

      state = normalise_materials(state, recipe)

      key = generate_cache_key(state, rounds)
      cache = %{cache | contents: Map.put(cache.contents, key, result)}

      {result, cache, max_geodes}
    end
  end

  def try_to_build(type, state, cache, rounds, recipe, can_build_material, max_geodes, result) do
    if can_build(type, state, recipe) and can_build_material do
      state = state |> mine() |> build(type, recipe)

      {r, cache, max_geodes} =
        run_recipe(
          recipe,
          state,
          rounds - 1,
          cache,
          max_geodes,
          true,
          true,
          true
        )

      {max(result, r), cache, max_geodes, false}
    else
      {result, cache, max_geodes, true}
    end
  end

  defp calculate_max_possible(state, rounds) do
    {_, _, _, geodes} = state.materials
    {_, _, _, rgeode} = state.robots

    # so far + geodes produced by current + geodes produced if one robot created per remaining round
    geodes + rgeode * rounds + rounds * (rounds - 1) / 2
  end

  defp normalise_materials(state, recipe) do
    {max_ore, max_clay, max_obsidian} =
      Enum.reduce(Map.values(recipe), {0, 0, 0}, fn {o, c, ob}, {mo, mc, mob} ->
        {max(mo, o), max(mc, c), max(mob, ob)}
      end)

    {ore, clay, obsidian, geode} = state.materials
    {rore, rclay, robsidian, _} = state.robots

    ore = normalise_single(ore, max_ore, rore)
    clay = normalise_single(clay, max_clay, rclay)
    obsidian = normalise_single(obsidian, max_obsidian, robsidian)

    %{state | materials: {ore, clay, obsidian, geode}}
  end

  defp normalise_single(amount, max_required, num_robots) do
    if num_robots == max_required and amount > max_required do
      max_required
    else
      amount
    end
  end

  defp generate_cache_key(state, rounds) do
    {state.robots, state.materials, rounds}
  end

  defp can_build("ore", state, recipe) do
    {num_robots, _, _, _} = state.robots

    maximum =
      Enum.reduce(Map.values(recipe), 0, fn {o, _, _}, acc ->
        max(acc, o)
      end)

    case num_robots < maximum do
      false ->
        false

      true ->
        enough_materials(state.materials, recipe.ore)
    end
  end

  defp can_build("clay", state, recipe) do
    {_, num_robots, _, _} = state.robots

    maximum =
      Enum.reduce(Map.values(recipe), 0, fn {_, o, _}, acc ->
        max(acc, o)
      end)

    case num_robots < maximum do
      false ->
        false

      true ->
        enough_materials(state.materials, recipe.clay)
    end
  end

  defp can_build("obsidian", state, recipe) do
    {_, _, num_robots, _} = state.robots

    maximum =
      Enum.reduce(Map.values(recipe), 0, fn {_, _, o}, acc ->
        max(acc, o)
      end)

    case num_robots < maximum do
      false ->
        false

      true ->
        enough_materials(state.materials, recipe.obsidian)
    end
  end

  defp can_build("geode", state, recipe) do
    enough_materials(state.materials, recipe.geode)
  end

  defp enough_materials(materials, recipe) do
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

  defp mine(state) do
    {rore, rclay, robsidian, rgeode} = state.robots
    {ore, clay, obsidian, geode} = state.materials
    %{state | materials: {ore + rore, clay + rclay, obsidian + robsidian, geode + rgeode}}
  end

  defp build(state, type, recipe) do
    {rore, rclay, robsidian, rgeode} = state.robots
    {ore, clay, obsidian, geode} = state.materials

    case type do
      "ore" ->
        recipe = recipe.ore
        robots = {rore + 1, rclay, robsidian, rgeode}

        materials =
          {ore - elem(recipe, 0), clay - elem(recipe, 1), obsidian - elem(recipe, 2), geode}

        %{state | robots: robots, materials: materials}

      "clay" ->
        recipe = recipe.clay
        robots = {rore, rclay + 1, robsidian, rgeode}

        materials =
          {ore - elem(recipe, 0), clay - elem(recipe, 1), obsidian - elem(recipe, 2), geode}

        %{state | robots: robots, materials: materials}

      "obsidian" ->
        recipe = recipe.obsidian
        robots = {rore, rclay, robsidian + 1, rgeode}

        materials =
          {ore - elem(recipe, 0), clay - elem(recipe, 1), obsidian - elem(recipe, 2), geode}

        %{state | robots: robots, materials: materials}

      "geode" ->
        recipe = recipe.geode
        robots = {rore, rclay, robsidian, rgeode + 1}

        materials =
          {ore - elem(recipe, 0), clay - elem(recipe, 1), obsidian - elem(recipe, 2), geode}

        %{state | robots: robots, materials: materials}
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
