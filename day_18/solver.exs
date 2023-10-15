file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.reduce([], fn line, acc ->
    coords =
      line
      |> String.split(",")
      |> Enum.reduce([], fn ch, coords ->
         coords ++ [String.to_integer(ch)]
      end)
      |> List.to_tuple()

    acc ++ [coords]
  end)

defmodule Foo do
  def solve1(input_data) do
  end

  def solve2(input_data) do
  end
end

IO.inspect(input_data)

# {_, result} = Foo.solve1(input_data)

# IO.puts("Answer to part 1 = #{result.highest}")

# result = Foo.solve2(input_data)

# IO.puts("Answer to part 2 = #{result}")
