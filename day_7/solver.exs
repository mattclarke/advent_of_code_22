file = "input.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.to_list()
  |> tl()

defmodule Foo do
  def solve(input_data) do
    parse_command(input_data, [], %{})
  end

  defp parse_command([], stack, tree) do
    # No more commands, but need to pop the stack until empty
    case stack do
      [] ->
        tree

      _ ->
        {_, value} = Map.fetch(tree, stack)
        new_stack = tl(stack)
        new_tree = Map.update(tree, new_stack, value, fn current -> current + value end)
        parse_command([], new_stack, new_tree)
    end
  end

  defp parse_command([head | tail], stack, tree) do
    case head do
      "$ cd .." ->
        {_, value} = Map.fetch(tree, stack)
        new_stack = tl(stack)
        new_tree = Map.update(tree, new_stack, value, fn current -> current + value end)
        parse_command(tail, new_stack, new_tree)

      "$ cd " <> d ->
        parse_command(tail, [d | stack], tree)

      "dir " <> _ ->
        parse_command(tail, stack, tree)

      "$ ls" ->
        parse_command(tail, stack, tree)

      size_and_name ->
        [size, _] = String.split(size_and_name, " ")
        value = String.to_integer(size)
        new_tree = Map.update(tree, stack, value, fn current -> current + value end)
        parse_command(tail, stack, new_tree)
    end
  end
end

paths = Foo.solve(input_data)

result =
  paths
  |> Stream.filter(fn {_, value} -> value <= 100_000 end)
  |> Enum.reduce(0, fn {_, value}, acc ->
    acc + value
  end)

IO.puts("Answer to part 1 = #{result}")

total_size = 70_000_000
target = 30_000_000
{_, size_used} = Map.fetch(paths, [])
required = target - (total_size - size_used)

[result | _] =
  Map.values(paths)
  |> Stream.filter(fn value -> value >= required end)
  |> Enum.sort()

IO.puts("Answer to part 2 = #{result}")
