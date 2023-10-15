file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.reduce(MapSet.new(), fn line, acc ->
    coords =
      line
      |> String.split(",")
      |> Enum.reduce([], fn ch, coords ->
        coords ++ [String.to_integer(ch)]
      end)
      |> List.to_tuple()

    MapSet.put(acc, coords)
  end)

defmodule Foo do
  @directions [{-1, 0, 0}, {1, 0, 0}, {0, -1, 0}, {0, 1, 0}, {0, 0, -1}, {0, 0, 1}]

  def solve1(input_data) do
    count_adjacent_spaces_in_other_set(input_data, input_data, fn x -> x end, fn x -> x + 1 end)
  end

  def solve2(input_data) do
    {max_x, max_y, max_z} =
      input_data
      |> Enum.reduce({-1, -1, -1}, fn {x, y, z}, {mx, my, mz} ->
        {max(x, mx), max(y, my), max(z, mz)}
      end)

    water = find_water(input_data, MapSet.new(), {max_x + 1, max_y + 1, max_z + 1}, {-1, -1, -1})

    count_adjacent_spaces_in_other_set(input_data, water)
  end

  defp count_adjacent_spaces_in_other_set(
         current,
         other,
         true_func \\ fn x -> x + 1 end,
         false_func \\ fn x -> x end
       ) do
    current
    |> Enum.reduce(0, fn coord, acc ->
      @directions
      |> Enum.reduce(acc, fn dir, acc ->
        new_coord =
          {elem(coord, 0) + elem(dir, 0), elem(coord, 1) + elem(dir, 1),
           elem(coord, 2) + elem(dir, 2)}

        if MapSet.member?(other, new_coord) do
          true_func.(acc)
        else
          false_func.(acc)
        end
      end)
    end)
  end

  defp find_water(input_data, water, {max_x, max_y, max_z} = maxs, {x, y, z}) do
    water = MapSet.put(water, {x, y, z})

    @directions
    |> Enum.reduce(water, fn {dx, dy, dz}, water ->
      coord = {x + dx, y + dy, z + dz}

      cond do
        MapSet.member?(input_data, coord) ->
          water

        MapSet.member?(water, coord) ->
          water

        x + dx < -1 or x + dx > max_x ->
          water

        y + dy < -1 or y + dy > max_y ->
          water

        z + dz < -1 or z + dz > max_z ->
          water

        true ->
          find_water(input_data, water, maxs, coord)
      end
    end)
  end
end

result = Foo.solve1(input_data)
IO.puts("Answer to part 1 = #{result}")

result = Foo.solve2(input_data)

IO.puts("Answer to part 2 = #{result}")
