file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.map(fn x ->
    x
    |> String.replace(" -> ", ",")
    |> String.split(",")
    |> Stream.map(fn y ->
      y
      |> String.to_integer()
    end)
    |> Enum.chunk_every(2)
  end)

defmodule Foo do
  def solve(origin, rocks) do
    lowest =
      rocks
      |> Stream.map(&elem(&1, 1))
      |> Enum.max()

    end_condition = fn {_, y} ->
      y >= lowest
    end

    special_rule = fn _ -> false end

    drop_grain(origin, end_condition, rocks, 0, special_rule)
  end

  defp drop_grain(position = {x, y}, end_condition, rocks, count, special_rule) do
    below = {x, y + 1}
    below_left = {x - 1, y + 1}
    below_right = {x + 1, y + 1}

    cond do
      end_condition.(position) ->
        count

      !MapSet.member?(rocks, below) ->
        drop_grain(below, end_condition, rocks, count, special_rule)

      !MapSet.member?(rocks, below_left) ->
        drop_grain(below_left, end_condition, rocks, count, special_rule)

      !MapSet.member?(rocks, below_right) ->
        drop_grain(below_right, end_condition, rocks, count, special_rule)

      true ->
        rocks = MapSet.put(rocks, position)
        drop_grain({500, 0}, end_condition, rocks, count + 1, special_rule)
    end
  end

  def find_rocks(input, rocks) when length(input) == 1 do
    rocks
  end

  def find_rocks([head | tail], rocks) do
    [x1, y1] = head
    [x2, y2] = hd(tail)

    rocks =
      Enum.reduce(x1..x2, rocks, fn x, acc ->
        Enum.reduce(y1..y2, acc, fn y, acc ->
          MapSet.put(acc, {x, y})
        end)
      end)

    find_rocks(tail, rocks)
  end
end

rocks =
  input_data
  |> Enum.reduce(MapSet.new(), fn x, acc ->
    Foo.find_rocks(x, acc)
  end)

result = Foo.solve({500, 0}, rocks)

IO.puts("Answer to part 1 = #{result}")

# IO.puts("Answer to part 2 = #{result}")
