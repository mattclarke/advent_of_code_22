monkeys = %{
  0 => {[64], 0},
  1 => {[60, 84, 84, 65], 0},
  2 => {[52, 67, 74, 88, 51, 61], 0},
  3 => {[67, 72], 0},
  4 => {[80, 79, 58, 77, 68, 74, 98, 64], 0},
  5 => {[62, 53, 61, 89, 86], 0},
  6 => {[86, 89, 82], 0},
  7 => {[92, 81, 70, 96, 69, 84, 83], 0},
}

rules = %{
  0 => %{func: fn x -> x * 7 end, test: 13, true: 1, false: 3, inspections: 0},
  1 => %{func: fn x -> x + 7 end, test: 19, true: 2, false: 7, inspections: 0},
  2 => %{func: fn x -> x * 3 end, test: 5, true: 5, false: 7, inspections: 0},
  3 => %{func: fn x -> x + 3 end, test: 2, true: 1, false: 2, inspections: 0},
  4 => %{func: fn x -> x * x end, test: 17, true: 6, false: 0, inspections: 0},
  5 => %{func: fn x -> x + 8 end, test: 11, true: 4, false: 6, inspections: 0},
  6 => %{func: fn x -> x + 2 end, test: 7, true: 3, false: 0, inspections: 0},
  7 => %{func: fn x -> x + 4 end, test: 3, true: 4, false: 5, inspections: 0},
}

defmodule Foo do
  def solve(monkeys, rules, number_rounds, worry_adjuster) do
    1..number_rounds
    |> Enum.reduce(monkeys, fn _, acc ->
      perform_round(acc, rules, worry_adjuster)
    end)
  end

  defp perform_round(monkeys, rules, worry_adjuster) do
    inspect_items(monkeys, rules, 0, worry_adjuster)
  end

  defp inspect_items(monkeys, _rules, 8, _worry_adjuster) do
    monkeys
  end

  defp inspect_items(monkeys, rules, current, worry_adjuster) do
    {items, inspections} = Map.get(monkeys, current)
    r = Map.get(rules, current)
    new_monkeys =
      Enum.reduce(items, monkeys, fn x, acc ->
        {dest, worry} = inspect_item(x, r, worry_adjuster)
        {ditems, dinspections} = Map.get(acc, dest)
        %{acc | dest => {ditems ++ [worry], dinspections}}
      end)
    new_monkeys = %{new_monkeys | current => {[], inspections + length(items)}}
    inspect_items(new_monkeys, rules, current + 1, worry_adjuster)
  end

  defp inspect_item(item, rules, worry_adjuster) do
    new_worry = Kernel.trunc(rules.func.(item))
    new_worry = worry_adjuster.(new_worry)
    case rem(new_worry, rules.test) do
      0 -> {rules.true, new_worry}
      _ -> {rules.false, new_worry}
    end
  end
end

result =
  Foo.solve(monkeys, rules, 20, fn x -> Kernel.trunc(x / 3) end)
  |> Map.values()
  |> Stream.map(fn {_, v} -> v end)
  |> Enum.sort(:desc)
  |> Enum.take(2)
  |> Enum.reduce(1, fn x, acc -> x * acc end)

IO.puts("Answer to part 1 = #{result}")

lcm =
  rules
  |> Map.values()
  |> Stream.map(fn v -> v.test end)
  |> Enum.reduce(1, fn x, acc -> x * acc end)

result =
  Foo.solve(monkeys, rules, 10000, fn x -> rem(x, lcm) end)
  |> Map.values()
  |> Stream.map(fn {_, v} -> v end)
  |> Enum.sort(:desc)
  |> Enum.take(2)
  |> Enum.reduce(1, fn x, acc -> x * acc end)

IO.puts("Answer to part 2 = #{result}")
