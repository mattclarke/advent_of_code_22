file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.to_list()

moves =
  input_data
  |> Enum.filter(fn x -> Regex.match?(~r/^move/, x) end)
  |> Enum.map(fn x ->
    parts = String.split(x, " ")

    {String.to_integer(Enum.at(parts, 1)), String.to_integer(Enum.at(parts, 3)),
     String.to_integer(Enum.at(parts, 5))}
  end)

crates =
  input_data
  |> Enum.filter(fn x -> String.contains?(x, "[") end)
  |> Enum.map(fn x ->
    x
    |> String.codepoints()
    |> Enum.chunk_every(4)
    |> Enum.map(&Enum.join/1)
    |> Enum.map(&String.trim/1)
    |> Enum.map(fn x -> String.replace(x, ["[", "]"], "") end)
  end)
  |> Enum.zip_reduce([], &[&1 | &2])
  |> Enum.reverse()
  |> Enum.map(fn row ->
    row
    |> Enum.filter(fn x -> String.trim(x) != "" end)
  end)
  |> Enum.with_index(&{&2 + 1, &1})
  |> Map.new()

result =
  moves
  |> Enum.reduce(crates, fn {amount, from, to}, crates ->
    crates
    |> Map.update!(from, &Enum.drop(&1, amount))
    |> Map.update!(to, &((crates[from] |> Enum.take(amount) |> Enum.reverse()) ++ &1))
  end)
  |> Enum.reduce("", fn {_, xs}, acc -> acc <> hd(xs) end)

IO.puts("Answer to part 1 = #{result}")

result =
  moves
  |> Enum.reduce(crates, fn {amount, from, to}, crates ->
    crates
    |> Map.update!(from, &Enum.drop(&1, amount))
    |> Map.update!(to, &((crates[from] |> Enum.take(amount)) ++ &1))
  end)
  |> Enum.reduce("", fn {_, xs}, acc -> acc <> hd(xs) end)

IO.puts("Answer to part 2 = #{result}")
