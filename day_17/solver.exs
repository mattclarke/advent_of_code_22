file = "ex1.txt"

input_data =
  File.stream!(file)
  |> Stream.map(&String.replace(&1, "\n", ""))
  |> Enum.filter(fn x -> x != "" end)
  |> Enum.at(0)

defmodule Foo do
  @width 7
  @shapes {
    %{name: "horizontal bar", coords: [{0, 0}, {1, 0}, {2, 0}, {3, 0}], width: 4},
    %{name: "cross", coords: [{1, 0}, {0, 1}, {1, 1}, {2, 1}, {1, 2}], width: 3},
    %{name: "l-shape", coords: [{0, 0}, {1, 0}, {2, 0}, {2, 1}, {2, 2}], width: 3},
    %{name: "vertical bar", coords: [{0, 0}, {0, 1}, {0, 2}, {0, 3}], width: 1},
    %{name: "square", coords: [{0, 0}, {1, 0}, {0, 1}, {1, 1}], width: 2}
  }

  def solve1(input_data) do
    place_shape(input_data, 3, 0, %{highest: 0, layout: MapSet.new()})
  end

  def place_shape(input_data, shape_index, wind_index, state) do
    shape = elem(@shapes, rem(shape_index, 5))
    y = state.highest + 3
    x = 2
    wind_direction = String.at(input_data, rem(wind_index, String.length(input_data)))

    x = apply_wind(x, wind_direction, shape)
    x = apply_wind(x, wind_direction, shape)
    x = apply_wind(x, wind_direction, shape)
    x = apply_wind(x, wind_direction, shape)
    x = apply_wind(x, wind_direction, shape)
    x = apply_wind(x, wind_direction, shape)
    draw(shape, x, y, state)
  end

  def apply_wind(x, direction, shape) do
    case direction do
      ">" ->
        max_x = @width - shape.width + 1
        min(max_x, x + 1)

      "<" ->
        max(0, x - 1)
    end
  end

  def draw(shape, x, y, state) do
    layout =
      Enum.reduce(shape.coords, state.layout, fn {c, r}, acc ->
        MapSet.put(acc, {x + c, y + r})
      end)

    Enum.each((state.highest + 6)..0, fn r ->
      IO.write("|")

      Enum.each(0..@width, fn c ->
        if MapSet.member?(layout, {c, r}) do
          IO.write("#")
        else
          IO.write(".")
        end
      end)

      IO.puts("|")
    end)
    IO.puts("+--------+")
  end
end

result = Foo.solve1(input_data)

# IO.puts("Answer to part 1 = #{result}")
