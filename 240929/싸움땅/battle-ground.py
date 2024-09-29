import sys

# 입력 처리
N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

# arr의 각 요소를 set으로 변환
for i in range(N):
    for j in range(N):
        arr[i][j] = {arr[i][j]} if arr[i][j] > 0 else set()

board = [[0] * N for _ in range(N)]  # 플레이어 맵
plyer = [0] * (M + 1)  # x, y, d, s 초기화

# 플레이어 정보 입력 처리
for i in range(1, M + 1):
    x, y, d, s = map(int, input().split())
    x, y = x - 1, y - 1  # 인덱스 1 감소
    board[x][y] = i  # 플레이어 위치 표시
    plyer[i] = [x, y, d, s]

# 점수 및 총 정보
points = [0] * (M + 1)
gun = [0] * (M + 1)

def get_gun(idx, x, y): 
    if len(arr[x][y]) > 0:
        mx = max(arr[x][y])
        if gun[idx] < mx:
            if gun[idx] > 0:
                arr[x][y].add(gun[idx])
            arr[x][y].remove(mx)
            gun[idx] = mx

def in_range(i, j):
    return 0 <= i < N and 0 <= j < N

dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
op = {0: 2, 1: 3, 2: 0, 3: 1}

for k in range(K):
    for m in range(1, M + 1):  # 플레이어 순차적으로
        si, sj, sd, pwr = plyer[m][0], plyer[m][1], plyer[m][2], plyer[m][3]
        
        # [1] 플레이어 이동 -> 격자 나가면 반대 방향으로 한 칸 이동
        ni, nj = si + dir[sd][0], sj + dir[sd][1]
        if not in_range(ni, nj):
            ni, nj = si + dir[op[sd]][0], sj + dir[op[sd]][1]  # 반대 방향으로
            plyer[m][2] = op[sd]

        # 이동한 칸으로 플레이어 정보 갱신
        plyer[m][0], plyer[m][1] = ni, nj
        board[si][sj] = 0  # 이동 전 위치 초기화

        # [2] 이동 후 처리
        if board[ni][nj] == 0:
            # 빈칸인 경우: 총을 확인하고 획득
            get_gun(m, ni, nj)
            board[ni][nj] = m  # 새로운 위치에 플레이어 배치
            continue
        else:
            # [3] 싸움 로직: 다른 플레이어가 있는 경우 싸움
            pi = board[ni][nj]  # 상대방 플레이어
            opponent_pwr = plyer[pi][3] + gun[pi]
            my_pwr = pwr + gun[m]

            # 승리자와 패배자 결정
            if (opponent_pwr > my_pwr) or (opponent_pwr == my_pwr and plyer[pi][3] > pwr):
                widx, lidx = pi, m
            else:
                widx, lidx = m, pi

            # 점수 획득
            reward = abs((plyer[widx][3] + gun[widx]) - (plyer[lidx][3] + gun[lidx]))
            points[widx] += reward

            # 패배자는 총을 놓고 이동
            li, lj, ld = plyer[lidx][0], plyer[lidx][1], plyer[lidx][2]
            if gun[lidx]:
                arr[li][lj].add(gun[lidx])
            gun[lidx] = 0

            # 패배자는 빈칸으로 이동 (시계 방향으로 회전하며 빈칸 찾기)
            for k in range(4):
                nni, nnj = ni + dir[(ld + k) % 4][0], nj + dir[(ld + k) % 4][1]
                if in_range(nni, nnj) and board[nni][nnj] == 0:
                    get_gun(lidx, nni, nnj)
                    board[nni][nnj] = lidx
                    plyer[lidx][0], plyer[lidx][1] = nni, nnj
                    plyer[lidx][2] = (ld + k) % 4
                    break

            # 승리자는 총 획득
            get_gun(widx, ni, nj)
            board[ni][nj] = widx
            plyer[widx][0], plyer[widx][1] = ni, nj

# 결과 출력: 각 플레이어의 점수 출력
for p in points[1:]:
    print(p, end=' ')