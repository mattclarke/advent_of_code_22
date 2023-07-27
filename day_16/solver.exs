file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.reduce(%{}, fn x, acc ->
    [valve, flow | tunnels] =
      x
      |> String.split([" ", "=", ";", ", "])
      |> Enum.filter(&String.match?(&1, ~r/^[-0-9|A-Z]+$/))

    Map.put(acc, valve, {String.to_integer(flow), tunnels})
  end)

defmodule Foo do
  def solve1(input_data, openable, minutes \\ 30) do
    explore("AA", input_data, 0, [], %{}, minutes, openable)
  end

  defp explore(_, _input_data, score, _opened, cache, 1, _openable) do
    {score, cache}
  end

  defp explore(current, input_data, score, opened, cache, minute, openable) do
    cache_value = Map.get(cache, {current, opened, minute})

    if cache_value != nil do
      {cache_value, cache}
    else
      {flow, tunnels} = Map.get(input_data, current)
      max_score = 0

      {max_score, cache} =
        if MapSet.member?(openable, current) do
          {opened, openable, score} = open_valve(current, opened, openable, score, minute, flow)

          explore_tunnels(
            [current],
            input_data,
            cache,
            opened,
            openable,
            minute,
            score,
            max_score
          )
        else
          {max_score, cache}
        end

      {max_score, cache} =
        explore_tunnels(tunnels, input_data, cache, opened, openable, minute, score, max_score)

      cache = Map.put(cache, {current, opened, minute}, max_score)
      {score, cache}
    end
  end

  def open_valve(current, opened, openable, score, minute, flow) do
    {opened ++ [current], MapSet.delete(openable, current), score + flow * (minute - 1)}
  end

  def explore_tunnels(tunnels, input_data, cache, opened, openable, minute, score, max_score) do
    tunnels
    |> Enum.reduce({max_score, cache}, fn x, {max_score, cache} ->
      {new_score, cache} = explore(x, input_data, score, opened, cache, minute - 1, openable)
      {max(new_score, max_score), cache}
    end)
  end

  def solve2(cache) do
    keys = Map.keys(cache)
    find_best_combination(keys, tl(keys), cache, 0)
  end

  def find_best_combination([_head | []], _, _, best) do
    best
  end

  def find_best_combination([_head | tail], [], cache, best) do
    find_best_combination(tail, tl(tail), cache, best)
  end

  def find_best_combination(first = [valves1 | _], [valves2 | tail], cache, best) do
    if MapSet.intersection(valves1, valves2) == MapSet.new() do
      pressure1 = Map.get(cache, valves1)
      pressure2 = Map.get(cache, valves2)
      find_best_combination(first, tail, cache, max(best, pressure1 + pressure2))
    else
      find_best_combination(first, tail, cache, best)
    end
  end
end

openable =
  input_data
  |> Enum.filter(fn {_, {flow, _}} ->
    flow > 0
  end)
  |> Enum.map(&elem(&1, 0))

{_, cache} = Foo.solve1(input_data, MapSet.new(openable))
result = Map.values(cache) |> Enum.reduce(0, &max/2)

IO.puts("Answer to part 1 = #{result}")

{_, cache} = Foo.solve1(input_data, MapSet.new(openable), 26)

# Go through the cache and find the best result for a particular set of valves
# and throw away the rest.
best_cache =
  cache
  |> Enum.reduce(%{}, fn x, acc ->
    {{_, valves, _}, value} = x
    as_set = MapSet.new(valves)
    Map.put(acc, as_set, max(Map.get(acc, as_set, 0), value))
  end)

result = Foo.solve2(best_cache)

IO.puts("Answer to part 2 = #{result}")
