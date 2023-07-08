file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Stream.take(1)
  |> Enum.at(0)
  |> String.graphemes()

defmodule Foo do
  def solve(data, packet_size) do
    {_, result} =
      data
      |> Stream.chunk_every(packet_size, 1, :discard)
      |> Stream.with_index(packet_size)
      |> Stream.filter(fn {x, _} ->
        length(Enum.uniq(x)) == packet_size
      end)
      |> Stream.take(1)
      |> Enum.at(0)

    result
  end
end

result = Foo.solve(input_data, 4)
IO.puts("Answer to part 1 = #{result}")

result = Foo.solve(input_data, 14)
IO.puts("Answer to part 2 = #{result}")
