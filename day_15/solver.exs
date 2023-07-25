file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.map(fn x ->
    x
    |> String.replace("Sensor at x=", "")
    |> String.replace(" y=", "")
    |> String.replace(": closest beacon is at x=", ",")
    |> String.split(",")
    |> Stream.map(&String.to_integer/1)
    |> Stream.chunk_every(2)
    |> Enum.map(&List.to_tuple/1)
  end)

defmodule Foo do
  def solve(input_data, target_row) do
    occupied =
      input_data
      |> Enum.reduce(MapSet.new(), fn [sensor, beacon], acc ->
        acc |> MapSet.put(sensor) |> MapSet.put(beacon)
      end)

    input_data
    |> Enum.reduce(MapSet.new(), fn [sensor, beacon], acc ->
      examine_sensor(sensor, beacon, target_row, occupied, acc)
    end)
  end

  defp examine_sensor(sensor = {sx, sy}, beacon, target_row, occupied, not_empty) do
    manhatten = calculate_manhatten_distance(sensor, beacon)

    cond do
      abs(target_row - sy) > manhatten ->
        not_empty

      true ->
        leftover = manhatten - abs(target_row - sy)

        (sx - leftover)..(sx + leftover)
        |> Enum.filter(fn x ->
          !MapSet.member?(occupied, {x, target_row})
        end)
        |> Enum.reduce(not_empty, fn x, acc ->
          MapSet.put(acc, x)
        end)
    end
  end

  defp calculate_manhatten_distance({sx, sy}, {bx, by}) do
    abs(sx - bx) + abs(sy - by)
  end
end

result = MapSet.size(Foo.solve(input_data, 2_000_000))

IO.puts("Answer to part 1 = #{result}")
