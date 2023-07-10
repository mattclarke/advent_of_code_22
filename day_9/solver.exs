file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Stream.map(&String.split(&1, " "))
  |> Stream.map(&List.to_tuple/1)
  |> Stream.map(fn {x, y} -> {x, String.to_integer(y)} end)
  |> Enum.to_list()

defmodule Foo do
  def solve(input_data, rope_length) do
    knots =
      1..rope_length
      |> Enum.reduce([], fn _, acc -> [{0, 0} | acc] end)

    do_instruction(input_data, knots, MapSet.new())
  end

  defp do_instruction([], _, visited) do
    visited
  end

  defp do_instruction([{direction, steps} | tail], knots, visited) do
    {new_knots, new_visited} = move_head(direction, steps, knots, visited)
    do_instruction(tail, new_knots, new_visited)
  end

  defp move_head(_, 0, knots, visited) do
    {knots, visited}
  end

  defp move_head(direction, steps, [head | tail], visited) do
    new_head = step_head(head, direction)
    new_tail = update_followers([new_head | tail])
    knots = [new_head | new_tail]
    visited = MapSet.put(visited, List.last(knots))
    move_head(direction, steps - 1, knots, visited)
  end

  defp update_followers([_ | _]) do
    []
  end

  defp update_followers([first, second | tail]) do
    second = step_tail(first, second)
    result = update_followers([second | tail])
    [second | result]
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

result = Foo.solve(input_data, 2)
IO.puts("Answer to part 1 = #{MapSet.size(result)}")

result = Foo.solve(input_data, 10)
IO.puts("Answer to part 2 = #{MapSet.size(result)}")
