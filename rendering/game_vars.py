import math

segments = []
screen = None
background = None
sprites = None
resolution = None
roadWidth = 2000
segmentLength = 200
rumbleLength = 3
trackLength = 0
lanes = 3
fieldOfView = 100
cameraHeight = 1000
cameraDepth = 1 / math.tan((fieldOfView / 2) * math.pi / 180)
drawDistance = 200
segment_count = 600
playerX = 0
playerZ = (cameraHeight * cameraDepth)
fogDensity = 3
position = 0
speed = 0
maxSpeed = segmentLength/(1/60)
accel = maxSpeed / 5
breaking = -maxSpeed
decel = -maxSpeed / 5
offRoadDecel = -maxSpeed / 2
offRoadLimit = maxSpeed / 4
centrifugal = 0.37
total_cars = 30
dt = 1 / 30
cars = []
player = None
background_sprite_group = None
player_sprite_group = None
track = None
gameStart = False

bg_sky_left = None
bg_sky_mid = None
bg_sky_right = None

bg_hills_left = None
bg_hills_mid = None
bg_hills_right = None

bg_tree_left = None
bg_tree_mid = None
bg_tree_right = None

sky_offset = 0.0
hill_offset = 0.0
tree_offset = 0.0
skySpeed = 0.001
hillSpeed = 0.002
treeSpeed = 0.003

paused = False
escape = False