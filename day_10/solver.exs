file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Stream.map(&String.split(&1, " "))
  |> Stream.map(&List.to_tuple/1)
  |> Stream.map(fn x ->
    case x do
      {a, b} -> {a, String.to_integer(b)}
      a -> a
    end
  end)
  |> Enum.to_list()

defmodule Foo do
  def solve(input_data) do
    state = %{cycle: 1, x: 1, result: %{}}
    Enum.reduce(input_data, state, &applesauce/2)
  end

  def applesauce({"addx", num}, %{cycle: cycle, x: x, result: result}) do
    result = Map.put(result, cycle + 1, x)
    %{cycle: cycle + 2, x: x + num, result: Map.put(result, cycle + 2, x + num)}
  end

  def applesauce({"noop"}, %{cycle: cycle, x: x, result: result}) do
    %{cycle: cycle + 1, x: x, result: Map.put(result, cycle + 1, x)}
  end
end

%{result: result} = Foo.solve(input_data)

total =
  [20, 60, 100, 140, 180, 220]
  |> Enum.reduce(0, fn x, acc ->
    acc + Map.get(result, x) * x
  end)

IO.puts("Answer to part 1 = #{total}")

# {_, result} = Foo.solve(input_data, 10)
# IO.puts("Answer to part 2 = #{MapSet.size(result)}")
