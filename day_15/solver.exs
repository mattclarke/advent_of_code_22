file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.map(fn x ->
    x
    |> String.split(["=", ",", ":"])
    |> Enum.filter(&String.match?(&1, ~r/^[-0-9]+$/))
    |> Enum.map(&String.to_integer/1)
    |> Enum.chunk_every(2)
    |> Enum.map(&List.to_tuple/1)
  end)

defmodule Foo do
  def solve1(input_data, target_row) do
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

  def solve2(input_data, size) do
    sensors_to_manhatten =
      Enum.reduce(input_data, %{}, fn [sensor, beacon], acc ->
        Map.put(acc, sensor, calculate_manhatten_distance(sensor, beacon))
      end)

    check_row(0, 0, sensors_to_manhatten, size)
  end

  defp check_row(x, y, sensors, size) when x >= size do
    check_row(0, y + 1, sensors, size)
  end

  defp check_row(x, y, sensors, size) do
    new_step =
      Enum.reduce(sensors, 0, fn sensor, acc ->
        {{sx, sy}, manhatten_distance} = sensor

        if in_range(x, y, {sx, sy}, manhatten_distance) do
          max(sx + (manhatten_distance - abs(y - sy) + 1) - x, acc)
        else
          acc
        end
      end)

    if new_step == 0 do
      {x + new_step, y}
    else
      check_row(x + new_step, y, sensors, size)
    end
  end

  defp in_range(x, y, {sx, sy}, manhatten_distance) do
    cond do
      abs(x - sx) + abs(y - sy) > manhatten_distance -> false
      true -> true
    end
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

result = MapSet.size(Foo.solve1(input_data, 2_000_000))

IO.puts("Answer to part 1 = #{result}")

{x, y} = Foo.solve2(input_data, 4_000_000)
result = 4_000_000 * x + y

IO.puts("Answer to part 2 = #{result}")
