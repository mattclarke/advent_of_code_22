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
  def solve(input_data, start_point, end_point) do
    explore(start_point, input_data, end_point, 0, MapSet.new())
  end

  defp explore(position, _, end_point, num_steps, _) when position == end_point do
    num_steps
  end

  defp explore(position, input_data, end_point, num_steps, seen) do
    IO.inspect(num_steps)
    seen = MapSet.put(seen, position)
    result = 1_000_000

    result =
      if can_move_north?(position, input_data, seen) do
        {c, r} = position
        min(result, explore({c, r - 1}, input_data, end_point, num_steps + 1, seen))
      else
        result
      end

    result =
      if can_move_south?(position, input_data, seen) do
        {c, r} = position
        min(result, explore({c, r + 1}, input_data, end_point, num_steps + 1, seen))
      else
        result
      end

    result =
      if can_move_east?(position, input_data, seen) do
        {c, r} = position
        min(result, explore({c + 1, r}, input_data, end_point, num_steps + 1, seen))
      else
        result
      end

    result =
      if can_move_west?(position, input_data, seen) do
        {c, r} = position
        min(result, explore({c - 1, r}, input_data, end_point, num_steps + 1, seen))
      else
        result
      end

    result
  end

  defp can_move_north?({c, r}, input_data, seen) do
    cond do
      !Map.has_key?(input_data, {c, r - 1}) -> false
      MapSet.member?(seen, {c, r - 1}) -> false
      Map.get(input_data, {c, r - 1}) - Map.get(input_data, {c, r}) > 1 -> false
      true -> true
    end
  end

  defp can_move_south?({c, r}, input_data, seen) do
    cond do
      !Map.has_key?(input_data, {c, r + 1}) -> false
      MapSet.member?(seen, {c, r + 1}) -> false
      Map.get(input_data, {c, r + 1}) - Map.get(input_data, {c, r}) > 1 -> false
      true -> true
    end
  end

  defp can_move_east?({c, r}, input_data, seen) do
    cond do
      !Map.has_key?(input_data, {c + 1, r}) -> false
      MapSet.member?(seen, {c + 1, r}) -> false
      Map.get(input_data, {c + 1, r}) - Map.get(input_data, {c, r}) > 1 -> false
      true -> true
    end
  end

  defp can_move_west?({c, r}, input_data, seen) do
    cond do
      !Map.has_key?(input_data, {c - 1, r}) -> false
      MapSet.member?(seen, {c - 1, r}) -> false
      Map.get(input_data, {c - 1, r}) - Map.get(input_data, {c, r}) > 1 -> false
      true -> true
    end
  end
end

result = Foo.solve(input_data, start_point, end_point)

IO.puts("Answer to part 1 = #{result}")
