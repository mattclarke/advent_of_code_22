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
  def solve1(input_data) do
    explore("AA", input_data, 0, [], %{}, 0)
  end

  defp explore(_, _input_data, score, _opened, cache, 30) do
    {score, cache}
  end

  defp explore(current, input_data, score, opened, cache, minute) do
    cache_value = Map.get(cache, {current, opened, minute})

    if cache_value != nil do
      {cache_value, cache}
    else
      {flow, tunnels} = Map.get(input_data, current)
      max_score = 0

      {max_score, cache} =
        if flow > 0 and !Enum.member?(opened, current) do
          opened = opened ++ [current]
          score = score + flow * (30 - minute - 1)
          {new_score, cache} = explore(current, input_data, score, opened, cache, minute + 1)
          {max(new_score, max_score), cache}
        else
          {max_score, cache}
        end

      {max_score, cache} =
        tunnels
        |> Enum.reduce({max_score, cache}, fn x, {max_score, cache} ->
          {new_score, cache} = explore(x, input_data, score, opened, cache, minute + 1)
          {max(new_score, max_score), cache}
        end)

      cache = Map.put(cache, {current, opened, minute}, max_score)
      {score, cache}
    end
  end
end

{_, cache} = Foo.solve1(input_data)
result = Map.values(cache) |> Enum.reduce(0, &max/2)

IO.puts("Answer to part 1 = #{result}")
