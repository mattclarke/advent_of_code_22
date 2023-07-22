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

    seen =
      start_points
      |> Enum.map(fn x ->
        {x, 0}
      end)
      |> Enum.into(%{})

    explore(starts, input_data, end_point, seen)
  end

  defp explore([], _, _, seen) do
    seen
  end

  defp explore([head | tail], input_data, end_point, seen) do
    {{c, r}, count} = head

    {tail, seen} =
      if can_move_north?({c, r}, input_data, count, seen) do
        {tail ++ [{{c, r - 1}, count + 1}], Map.put(seen, {c, r - 1}, count + 1)}
      else
        {tail, seen}
      end

    {tail, seen} =
      if can_move_south?({c, r}, input_data, count, seen) do
        {tail ++ [{{c, r + 1}, count + 1}], Map.put(seen, {c, r + 1}, count + 1)}
      else
        {tail, seen}
      end

    {tail, seen} =
      if can_move_east?({c, r}, input_data, count, seen) do
        {tail ++ [{{c + 1, r}, count + 1}], Map.put(seen, {c + 1, r}, count + 1)}
      else
        {tail, seen}
      end

    {tail, seen} =
      if can_move_west?({c, r}, input_data, count, seen) do
        {tail ++ [{{c - 1, r}, count + 1}], Map.put(seen, {c - 1, r}, count + 1)}
      else
        {tail, seen}
      end

    explore(tail, input_data, end_point, seen)
  end

  defp can_move_north?({c, r}, input_data, num_steps, seen) do
    cond do
      !Map.has_key?(input_data, {c, r - 1}) -> false
      Map.get(seen, {c, r - 1}, 1_000_000) <= num_steps + 1 -> false
      Map.get(input_data, {c, r - 1}) - Map.get(input_data, {c, r}) > 1 -> false
      true -> true
    end
  end

  defp can_move_south?({c, r}, input_data, num_steps, seen) do
    cond do
      !Map.has_key?(input_data, {c, r + 1}) -> false
      Map.get(seen, {c, r + 1}, 1_000_000) <= num_steps + 1 -> false
      Map.get(input_data, {c, r + 1}) - Map.get(input_data, {c, r}) > 1 -> false
      true -> true
    end
  end

  defp can_move_east?({c, r}, input_data, num_steps, seen) do
    cond do
      !Map.has_key?(input_data, {c + 1, r}) -> false
      Map.get(seen, {c + 1, r}, 1_000_000) <= num_steps + 1 -> false
      Map.get(input_data, {c + 1, r}) - Map.get(input_data, {c, r}) > 1 -> false
      true -> true
    end
  end

  defp can_move_west?({c, r}, input_data, num_steps, seen) do
    cond do
      !Map.has_key?(input_data, {c - 1, r}) -> false
      Map.get(seen, {c - 1, r}, 1_000_000) <= num_steps + 1 -> false
      Map.get(input_data, {c - 1, r}) - Map.get(input_data, {c, r}) > 1 -> false
      true -> true
    end
  end
end

result = Map.get(Foo.solve(input_data, [start_point], end_point), end_point)
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

result = Map.get(Foo.solve(input_data, start_points, end_point), end_point)
IO.puts("Answer to part 2 = #{result}")
