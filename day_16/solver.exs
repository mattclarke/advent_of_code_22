file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.map(fn x ->
    [valve, flow | tunnels] =
      x
      |> String.split([" ", "=", ";", ", "])
      |> Enum.filter(&String.match?(&1, ~r/^[-0-9|A-Z]+$/))

    {valve, String.to_integer(flow), List.to_tuple(tunnels)}
  end)
  |> IO.inspect()

defmodule Foo do
  def solve1(input_data, target_row) do
  end
end

# IO.puts("Answer to part 1 = #{result}")
