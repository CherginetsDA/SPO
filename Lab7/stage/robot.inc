define range_it ranger
(
  sensor
  (
  range [0.0001 5]
  fov 360
  samples 360
  )
  color "black"
  size [0.05 0.05 0.1]
)

define robot position
(

      block
      (
            points 6
            point[0] [0.75 0]
            point[1] [1 0.25]
            point[2] [1 0.75]
            point[3] [0.75 1]
            point[4] [0 1]
            point[5] [0 0]
            z [0.01 0.2]
      )
      drive "diff"

      range_it
      (
      pose [ 0.75 0 -0.30 0]
      )
)
