# 문제 접근법
# 그런거 없고 그냥 문제에서 시키는 대로 구현하면 됌.
# 0. 초기 입력으로 주어진 상태에서 시작
# 1. 로봇이 현재 위치한 자리를 청소함.
# 2-1. 로봇이 바라보는 방향 기준 왼쪽(반시계방향)에 청소할 공간(0)이 있으면 그 쪽 방향으로 돌고, 이동한 후, 1번부터 다시 시작
# 2-2. 왼쪽에 청소할 공간이 없다면(이미 청소되어있거나 벽일 경우), 그쪽 방향으로 돌기만하고, 1번부터 다시 시작
# 2-3. 2-2를 계속 반복했는데 로봇기준으로 4방향 전부 청소할수 없는 공간이라면(이미 청소되어 있거나 벽일 경우), 바라보는 방향을 유지하는 상태로 뒤로 1칸 후진한 뒤, 1번부터 다시 시작
# 2-4. 2-3과 같은 상황인데 뒤에 벽일 경우(이미 청소한 공간은 이동할 수 있지만, 벽이면 막혀서 갈 수가 없음), 그대로 종료
# !!!!!!. 2-3에서 바라보는 방향을 유지한다는건 로봇이 맨 처음에 해당 위치에 도착했을 때 바라보단 방향을 얘기하는 거임

n, m = map(int, input().split())

# ㅅㅂ y좌표 , x좌표 순서임  +  # 청소기는 바라보는 방향이 있다.
robot_y, robot_x, robot_dir = map(int, input().split())

d = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # 북동남서
# d[(robot_dir-1) % 4] -> 로봇이 반시계로 회전하면 북서남동 순서대로 도는 것이고, 이를 처리해주기 위해 나머지연산 이용

# 맵 세팅
zone = []
for _ in range(n):
    zone.append(list(map(int, input().split())))

# robot_dir가 전역변수 처리가 안됌. global 쓰면 될 거 같긴한데, 그렇게 하기 싫음
# 북:0 동:1 남:2 서:3
# def turn_left():  # 왼쪽방향으로만 회전한다. 즉, 북 -> 서 -> 남 -> 동 -> 북 -> ...
#     robot_dir -= 1
#     robot_dir %= 4

# 청소한 칸 갯수
cleaned_space = 0

# count = 0 원래 쓰려다가 all()로 해결함

while True:
    # 1. 현재위치를 청소한다.
    if zone[robot_y][robot_x] == 0:
        cleaned_space += 1
        # 벽과 청소된 빈칸을 구분해야함. 청소된 빈칸은 후진해서 갈 수 있지만 벽은 갈 수 없기 때문
        zone[robot_y][robot_x] = -1

    # 주변에 청소할 수 있는 공간이 없을 경우 : 원래는 4번을 돌면서 count 변수에 +1 해서 4가 되었을 때, 체크하는 방식으로 하다가, 그냥 all()로 하는게 더 간결함
    if all(zone[robot_y+dy][robot_x+dx] != 0 for dx, dy in d):
        new_x, new_y = robot_x + d[(robot_dir-2) %
                                   4][0], robot_y + d[(robot_dir-2) % 4][1]
        if zone[new_y][new_x] == 1:  # 후진방향에 벽이 있으면 못감 (2-4의 케이스)
            break
        else:  # 벽이 아니면 방향 유지한채로 후진 (2-3의 케이스)
            robot_x, robot_y = new_x, new_y

    # 주변 4칸 중에 하나라도 청소할 수 있는 공간이 있을 경우, 거기가 어디인지 찾아야함
    else:
        # 현위치 기준, 바라보는 방향 기준 왼쪽 좌표(반시계 90도 방향)
        new_x, new_y = robot_x + d[(robot_dir-1) %
                                   4][0], robot_y + d[(robot_dir-1) % 4][1]

        # 왼쪽방향(새로운 좌표)에 청소할 공간이 있다면
        if zone[new_y][new_x] == 0:
            # 로봇이 해당 위치로 이동 (청소할 공간이 있는 경우에만 로봇이 이동함) -> 2-1의 케이스
            robot_x, robot_y = new_x, new_y

        # 이동 안해도 회전은 해야함
        robot_dir = (robot_dir-1) % 4  # 2-1과 2-2의 케이스 둘다 회전은 해야함


print(cleaned_space)
