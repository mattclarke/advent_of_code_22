file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Stream.filter(fn x ->
    x != ""
  end)
  |> Enum.map(fn x ->
    {result, _} = Code.eval_string(x)
    result
  end)

defmodule Foo do
  def solve(first, second) do
    compare(first, second)
  end

  defp compare([], []) do
    nil
  end

  defp compare([], [_ | _]) do
    true
  end

  defp compare([_ | _], []) do
    false
  end

  defp compare(first = [head1 | tail1], second = [head2 | tail2])
       when is_list(first) and is_list(second) do
    ans = compare(head1, head2)

    case ans do
      nil -> compare(tail1, tail2)
      _ -> ans
    end
  end

  defp compare(first, second) when is_integer(first) and is_integer(second) do
    cond do
      first < second -> true
      first > second -> false
      true -> nil
    end
  end

  defp compare(first, second) when is_integer(first) and is_list(second) do
    compare([first], second)
  end

  defp compare(first, second) when is_list(first) and is_integer(second) do
    compare(first, [second])
  end
end

result =
  input_data
  |> Enum.chunk_every(2)
  |> Enum.map(&List.to_tuple/1)
  |> Enum.map(fn {first, second} ->
    Foo.solve(first, second)
  end)
  |> Enum.with_index(1)
  |> Enum.filter(fn {v, _} ->
    v
  end)
  |> Enum.map(fn {_, i} ->
    i
  end)
  |> Enum.sum()

IO.puts("Answer to part 1 = #{result}")

input_data = [[[2]], [[6]]] ++ input_data

result =
  input_data
  |> Enum.sort(&Foo.solve/2)
  |> Enum.with_index(1)
  |> Enum.filter(fn {v, _} ->
    v == [[2]] or v == [[6]]
  end)
  |> Enum.map(fn {_, i} ->
    i
  end)
  |> Enum.reduce(1, fn x, acc ->
    acc * x
  end)

IO.puts("Answer to part 2 = #{result}")
