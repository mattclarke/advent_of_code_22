file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Stream.map(&String.replace(&1, ",", "-"))
  |> Stream.map(&String.split(&1, "-"))
  |> Stream.map(fn x ->
    x
    |> Stream.map(&String.to_integer/1)
    |> Enum.to_list()
    |> List.to_tuple()
  end)
  |> Enum.to_list()

contained? = fn {x1, x2, y1, y2} ->
  cond do
    x1 >= y1 and x2 <= y2 -> 1
    y1 >= x1 and y2 <= x2 -> 1
    true -> 0
  end
end

data =
  input_data
  |> Stream.map(&contained?.(&1))
  |> Enum.sum()

IO.puts("Answer to part 1 = #{data}")

overlaps? = fn {x1, x2, y1, y2} ->
  cond do
    Range.disjoint?(x1..x2, y1..y2) -> 0
    true -> 1
  end
  # cond do
  #   x1 <= y1 and x2 >= y1 -> 1
  #   x1 <= y2 and x2 >= y2 -> 1
  #   # Check if x is contained in y
  #   y1 <= x1 and y2 >= x2 -> 1
  #   true -> 0
  # end
end

data =
  input_data
  |> Stream.map(&overlaps?.(&1))
  |> Enum.sum()

IO.puts("Answer to part 2 = #{data}")
