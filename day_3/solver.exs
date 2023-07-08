file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Stream.map(&String.graphemes(&1))
  |> Enum.to_list()

convert_to_score = fn char ->
  value = :binary.first(char)

  if value >= :binary.first("a") do
    value - :binary.first("a") + 1
  else
    value - :binary.first("A") + 27
  end
end

find_match = fn comps ->
  comps
  |> Stream.map(&MapSet.new/1)
  |> Enum.reduce(&MapSet.intersection/2)
  |> Enum.at(0)
end

data =
  input_data
  |> Stream.map(fn x -> Enum.chunk_every(x, div(length(x), 2)) end)
  |> Stream.map(&find_match.(&1))
  |> Stream.map(&convert_to_score.(&1))
  |> Enum.sum()

IO.puts("Answer to part 1 = #{data}")

data =
  Stream.chunk_every(input_data, 3)
  |> Stream.map(&find_match.(&1))
  |> Stream.map(&convert_to_score.(&1))
  |> Enum.sum()

IO.puts("Answer to part 2 = #{data}")
