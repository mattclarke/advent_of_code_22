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
    input_data
    |> Enum.reduce(0, fn coord, acc ->
      @directions
      |> Enum.reduce(acc, fn dir, acc ->
        new_coord =
          {elem(coord, 0) + elem(dir, 0), elem(coord, 1) + elem(dir, 1),
           elem(coord, 2) + elem(dir, 2)}

        if MapSet.member?(input_data, new_coord) do
          acc
        else
          acc + 1
        end
      end)
    end)
  end

  def solve2(input_data) do
  end
end

result = Foo.solve1(input_data)
IO.puts("Answer to part 1 = #{result}")

# result = Foo.solve2(input_data)

# IO.puts("Answer to part 2 = #{result}")
