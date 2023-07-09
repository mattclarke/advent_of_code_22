file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Stream.map(&String.split(&1, " "))
  |> Stream.map(&List.to_tuple/1)
  |> Stream.map(fn {x, y} -> {x, String.to_integer(y)} end)
  |> Enum.to_list()

defmodule Foo do
  def solve1(input_data) do
    head_pos = {0, 0}
    tail_pos = {0, 0}

    visited =
      MapSet.new()
      |> MapSet.put(tail_pos)

    move_head(input_data, head_pos, tail_pos, visited)
  end

  def solve2(input_data) do
    knots =
      1..10
      |> Enum.reduce([], fn _, acc -> [{0, 0} | acc] end)

    do_instruction(input_data, knots, MapSet.new())
  end

  defp do_instruction([{direction, steps} | tail], knots, visited) do
    {new_knots, new_visited} = do_steps(direction, steps, knots, visited)
    do_instruction(tail, new_knots, new_visited)
  end

  defp do_instruction([], _, visited) do
    visited
  end

  defp do_steps(direction, steps, [head | tail], visited) do
    new_head = step_head(head, direction)
    new_tail = applesauce([new_head | tail])
    knots = [new_head | new_tail]
    visited = MapSet.put(visited, List.last(knots))
    if steps == 1 do
      {knots, visited}
    else
      do_steps(direction, steps - 1, knots, visited)
    end
  end

  defp applesauce([first | tail]) do
    if length(tail) > 0 do
      [second | tail] = tail
      second = step_tail(first, second)
      result = applesauce([second | tail])
      [second | result]
    else
      []
    end
  end

  defp applesauce([]) do
    []
  end

  defp move_head([{direction, steps} | tail], head_pos, tail_pos, visited) do
    {new_head_pos, new_tail_pos} = move_pair(direction, head_pos, tail_pos)
    new_visited = MapSet.put(visited, new_tail_pos)

    if steps == 1 do
      move_head(tail, new_head_pos, new_tail_pos, new_visited)
    else
      move_head([{direction, steps - 1} | tail], new_head_pos, new_tail_pos, new_visited)
    end
  end

  defp move_head([], _head_pos, _tail_pos, visited) do
    visited
  end

  defp move_pair(direction, head_pos, tail_pos) do
    new_head_pos = step_head(head_pos, direction)
    {new_head_pos, step_tail(new_head_pos, tail_pos)}
  end

  defp step_head(head_pos, direction) do
    case direction do
      "U" -> {elem(head_pos, 0), elem(head_pos, 1) + 1}
      "D" -> {elem(head_pos, 0), elem(head_pos, 1) - 1}
      "L" -> {elem(head_pos, 0) - 1, elem(head_pos, 1)}
      "R" -> {elem(head_pos, 0) + 1, elem(head_pos, 1)}
    end
  end

  defp step_tail(head_pos, tail_pos) do
    new_tail_pos =
      case {head_pos, tail_pos} do
        {{hx, hy}, {tx, ty}} when abs(hx - tx) <= 1 and abs(hy - ty) <= 1 -> tail_pos
        {{hx, hy}, {tx, ty}} when hx > tx and hy > ty -> {tx + 1, ty + 1}
        {{hx, hy}, {tx, ty}} when hx < tx and hy > ty -> {tx - 1, ty + 1}
        {{hx, hy}, {tx, ty}} when hx < tx and hy < ty -> {tx - 1, ty - 1}
        {{hx, hy}, {tx, ty}} when hx > tx and hy < ty -> {tx + 1, ty - 1}
        {{hx, _}, {tx, ty}} when hx > tx -> {tx + 1, ty}
        {{hx, _}, {tx, ty}} when hx < tx -> {tx - 1, ty}
        {{_, hy}, {tx, ty}} when hy > ty -> {tx, ty + 1}
        {{_, hy}, {tx, ty}} when hy < ty -> {tx, ty - 1}
      end

    new_tail_pos
  end
end

result = Foo.solve1(input_data)
IO.puts("Answer to part 1 = #{MapSet.size(result)}")

result = Foo.solve2(input_data)
IO.puts("Answer to part 2 = #{MapSet.size(result)}")
