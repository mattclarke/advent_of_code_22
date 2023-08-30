file = "ex1.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.filter(fn x -> x != "" end)
  |> Enum.at(0)

defmodule Foo do
  @width 7
  @shapes {
    %{name: "horizontal bar", coords: [{0, 0}, {1, 0}, {2, 0}, {3, 0}], width: 4, height: 1},
    %{name: "cross", coords: [{1, 0}, {0, 1}, {1, 1}, {2, 1}, {1, 2}], width: 3, height: 3},
    %{name: "l-shape", coords: [{0, 0}, {1, 0}, {2, 0}, {2, 1}, {2, 2}], width: 3, height: 3},
    %{name: "vertical bar", coords: [{0, 0}, {0, 1}, {0, 2}, {0, 3}], width: 1, height: 4},
    %{name: "square", coords: [{0, 0}, {1, 0}, {0, 1}, {1, 1}], width: 2, height: 2}
  }

  def solve1(input_data) do
    # Create a shape to represent the floor, so can use standard block collision to find floor
    initial_mapset =
      Enum.reduce(0..(@width - 1), MapSet.new(), fn x, acc ->
        MapSet.put(acc, {x, -1})
      end)

    state = %{highest: 0, layout: initial_mapset}

    Enum.reduce(0..2022, {0, state}, fn i, {wind_index, current_state} ->
      place_new_shape(input_data, i, wind_index, current_state)
    end)
  end

  def place_new_shape(input_data, shape_index, wind_index, state) do
    shape = elem(@shapes, rem(shape_index, 5))
    move_shape(2, state.highest + 3, shape, input_data, wind_index, state)
  end

  def move_shape(x, y, shape, input_data, wind_index, state) do
    wind_index = rem(wind_index, String.length(input_data))
    wind_direction = String.at(input_data, wind_index)

    x = apply_wind(x, y, wind_direction, shape, state)

    {moved_down, y} = try_moving_down(x, y, shape, state)

    if !moved_down do
      new_state =
        Enum.reduce(shape.coords, state, fn {c, r}, acc ->
          new_layout = MapSet.put(acc.layout, {x + c, y + r})
          new_highest = max(acc.highest, y + shape.height)
          %{acc | highest: new_highest, layout: new_layout}
        end)

      {wind_index + 1, new_state}
    else
      move_shape(x, y, shape, input_data, wind_index + 1, state)
    end
  end

  def apply_wind(x, y, direction, shape, state) do
    case direction do
      ">" ->
        if hits_something?(x, y, 1, 0, shape, state) do
          x
        else
          max_x = @width - 1 - shape.width + 1
          min(max_x, x + 1)
        end

      "<" ->
        if hits_something?(x, y, -1, 0, shape, state) do
          x
        else
          max(0, x - 1)
        end
    end
  end

  def try_moving_down(x, y, shape, state) do
    hits_something = hits_something?(x, y, 0, -1, shape, state)

    cond do
      hits_something -> {false, y}
      true -> {true, y - 1}
    end
  end

  def hits_something?(x, y, dx, dy, shape, state) do
    Enum.reduce(shape.coords, false, fn {c, r}, acc ->
      if MapSet.member?(state.layout, {x + dx + c, y + dy + r}) do
        true
      else
        acc
      end
    end)
  end

  def draw(shape, x, y, state) do
    layout =
      Enum.reduce(shape.coords, state.layout, fn {c, r}, acc ->
        MapSet.put(acc, {x + c, y + r})
      end)

    Enum.each((state.highest + 6)..0, fn r ->
      IO.write("|")

      Enum.each(0..(@width - 1), fn c ->
        if MapSet.member?(layout, {c, r}) do
          IO.write("#")
        else
          IO.write(".")
        end
      end)

      IO.puts("|")
    end)

    IO.puts("+-------+\n")
  end
end

{_, result} = Foo.solve1(input_data)

IO.puts("Answer to part 1 = #{result.highest}")
