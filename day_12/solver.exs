file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Stream.map(&String.graphemes/1)
  |> Enum.to_list()
  |> Stream.with_index()
  |> Enum.reduce(%{}, fn {x, r}, acc ->
    row_map =
      x
      |> Stream.with_index()
      |> Enum.map(fn {y, c} ->
        case y do
          "S" -> {"start", {c, r}}
          "E" -> {"end", {c, r}}
          y -> {{c, r}, :binary.first(y) - :binary.first("a")}
        end
      end)
      |> Enum.into(%{})

    Map.merge(acc, row_map)
  end)

start_point = Map.get(input_data, "start")
end_point = Map.get(input_data, "end")
input_data = Map.put(input_data, start_point, 0)
input_data = Map.put(input_data, end_point, 25)

defmodule Foo do
  def solve(input_data, start_points, end_point) do
    starts =
      Enum.reduce(start_points, [], fn x, acc ->
        [{x, 0} | acc]
      end)

    seen = MapSet.new(start_points)

    explore(starts, input_data, end_point, seen)
  end

  defp explore([{pos, count} | _], _, end_point, _) when pos == end_point do
    count
  end

  defp explore([head | tail], input_data, end_point, seen) do
    {{c, r}, count} = head

    {tail, seen} =
      [{c, r - 1}, {c, r + 1}, {c + 1, r}, {c - 1, r}]
      |> Enum.reduce({tail, seen}, fn new_pos, {new_tail, new_seen} ->
        if can_move({c, r}, new_pos, input_data, seen) do
        {new_tail ++ [{new_pos, count + 1}], MapSet.put(new_seen, new_pos)}
        else
          {new_tail, new_seen}
        end
      end)

    explore(tail, input_data, end_point, seen)
  end
  
  defp can_move(current_pos, new_pos, input_data, seen) do
    cond do
      !Map.has_key?(input_data, new_pos) -> false
      MapSet.member?(seen, new_pos) -> false
      Map.get(input_data, new_pos) - Map.get(input_data, current_pos) > 1 -> false
      true -> true
    end
  end
end

result = Foo.solve(input_data, [start_point], end_point)
IO.puts("Answer to part 1 = #{result}")

start_points =
  input_data
  |> Enum.filter(fn {_, v} ->
    v == 0
  end)
  |> Enum.map(fn {k, _} ->
    k
  end)
  |> Enum.to_list()

result = Foo.solve(input_data, start_points, end_point)
IO.puts("Answer to part 2 = #{result}")
