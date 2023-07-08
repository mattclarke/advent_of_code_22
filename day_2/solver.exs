file = "input.txt"

input_data = File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.to_list()


calc_score = fn
  ["A", "X"] -> 1 + 3
  ["A", "Y"] -> 2 + 6
  ["A", "Z"] -> 3 + 0
  ["B", "X"] -> 1 + 0
  ["B", "Y"] -> 2 + 3
  ["B", "Z"] -> 3 + 6
  ["C", "X"] -> 1 + 6
  ["C", "Y"] -> 2 + 0
  ["C", "Z"] -> 3 + 3
end


data =
  input_data
  |> Stream.map(&calc_score.(String.split(&1, " ")))
  |> Enum.sum()

IO.puts("Answer to part 1 = #{data}")

calc_score = fn
  ["A", "X"] -> 3 + 0
  ["A", "Y"] -> 1 + 3
  ["A", "Z"] -> 2 + 6
  ["B", "X"] -> 1 + 0
  ["B", "Y"] -> 2 + 3
  ["B", "Z"] -> 3 + 6
  ["C", "X"] -> 2 + 0
  ["C", "Y"] -> 3 + 3
  ["C", "Z"] -> 1 + 6
end


data =
  input_data
  |> Stream.map(&calc_score.(String.split(&1, " ")))
  |> Enum.sum()

IO.puts("Answer to part 2 = #{data}")
