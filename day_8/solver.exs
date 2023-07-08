file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Stream.map(&String.graphemes/1)
  |> Stream.map(fn row ->
    row
    |> Enum.map(&String.to_integer/1)
  end)
  |> Enum.to_list()

defmodule Foo do
  def solve1(input_data) do
    # From West
    {from_west, _} =
      input_data
      |> Enum.with_index()
      |> Enum.reduce({MapSet.new(), %{}}, fn {x, r}, {seen, best_row} ->
        z = Enum.zip(x, Enum.to_list(0..99))
        {sr, br} = from_west(z, r, -1, seen, best_row)
        {MapSet.union(sr, seen), br}
      end)

    # From East
    {from_east, _} =
      input_data
      |> Enum.with_index()
      |> Enum.reverse()
      |> Enum.reduce({MapSet.new(), %{}}, fn {x, r}, {seen, best_row} ->
        z = Enum.zip(x, Enum.to_list(0..99))
        {sr, br} = from_west(Enum.reverse(z), r, -1, seen, best_row)
        {MapSet.union(sr, seen), br}
      end)

    MapSet.union(from_west, from_east)
  end

  defp from_north(head, row, column, seen, best_row) do
    if head > Map.get(best_row, column, -1) do
      seen = MapSet.put(seen, {column, row})
      best_row = Map.update(best_row, column, head, fn _ -> head end)
      {seen, best_row}
    else
      {seen, best_row}
    end
  end

  defp from_west([{head, column} | tail], row, height, seen, best_row) do
    if head > height do
      {seen, best_row} = from_north(head, row, column, seen, best_row)
      seen = MapSet.put(seen, {column, row})
      from_west(tail, row, head, seen, best_row)
    else
      {seen, best_row} = from_north(head, row, column, seen, best_row)
      from_west(tail, row, height, seen, best_row)
    end
  end

  defp from_west([], _, _, seen, best_row) do
    {seen, best_row}
  end

  def solve2(tree_map) do
    tree_map
    |> Stream.map(fn {{col, row}, val} ->
      l = go_left(tree_map, row, col - 1, val, 0)
      r = go_right(tree_map, row, col + 1, val, 0)
      u = go_up(tree_map, row - 1, col, val, 0)
      d = go_down(tree_map, row + 1, col, val, 0)
      l * r * u * d
    end)
    |> Enum.max()
  end

  defp go_left(tree_map, r, c, height, count) do
    case c do
      -1 ->
        count

      col ->
        {_, next_tree} = Map.fetch(tree_map, {col, r})

        if next_tree >= height do
          count + 1
        else
          go_left(tree_map, r, col - 1, height, count + 1)
        end
    end
  end

  defp go_right(tree_map, r, c, height, count) do
    case c do
      99 ->
        count

      col ->
        {_, next_tree} = Map.fetch(tree_map, {col, r})

        if next_tree >= height do
          count + 1
        else
          go_right(tree_map, r, col + 1, height, count + 1)
        end
    end
  end

  defp go_up(tree_map, r, c, height, count) do
    case r do
      -1 ->
        count

      row ->
        {_, next_tree} = Map.fetch(tree_map, {c, row})

        if next_tree >= height do
          count + 1
        else
          go_up(tree_map, row - 1, c, height, count + 1)
        end
    end
  end

  defp go_down(tree_map, r, c, height, count) do
    case r do
      99 ->
        count

      row ->
        {_, next_tree} = Map.fetch(tree_map, {c, row})

        if next_tree >= height do
          count + 1
        else
          go_down(tree_map, row + 1, c, height, count + 1)
        end
    end
  end
end

result = Foo.solve1(input_data)

IO.puts("Answer to part 1 = #{MapSet.size(result)}")

tree_map =
  input_data
  |> Stream.with_index()
  |> Enum.reduce(%{}, fn {x, r}, acc1 ->
    row_map =
      x
      |> Stream.with_index()
      |> Enum.map(fn {y, c} ->
        {{c, r}, y}
      end)
      |> Enum.into(%{})

    Map.merge(acc1, row_map)
  end)

result = Foo.solve2(tree_map)

IO.puts("Answer to part 2 = #{result}")
