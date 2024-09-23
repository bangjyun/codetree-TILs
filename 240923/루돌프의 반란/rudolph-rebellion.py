def main():
    N,M,P,C,D = map(int,input().split())
    Rr,Rc=map(int,input().split())
    board = Board(N, M, P, C, D, Rr, Rc)


    for _ in range(P):
        num,Sr,Sc=map(int,input().split())
        board.a[Sr-1][Sc-1]=num-1
        board.santa_coord[num-1]=(Sr-1,Sc-1)
    for m in range(M):
        board.roudolf()
        for p in range(P):
            board.santa(p)

        if board.outSanta==P:
            break
        for s in board.score:
            print(s,end=" ")
        print("/n")
    # print(board)
    # for s in board.score:
    #     print(s,end=" ")



class Board():
    def __init__(self, N, M, P, C, D, Rr, Rc):
        self.N = N
        self.M = M
        self.P = P
        self.C = C
        self.D = D
        self.Rr = Rr - 1
        self.Rc = Rc - 1
        self.a=[[0]*N for _ in range(N)]
        self.score=[0]*P 
        self.is_sleep=[False]*P 
        # self.santa_coord =[0]*P 
        self.santa_coord =[(0,0)]*P 
        self.outSanta=0
    
    def in_range(self,r,c):
        return 0<=r<self.N and 0<=c<self.N 
    
    def cal_dist(self,rr,rc,sr,sc):
        return ((rr-sr)**2+(rc-sc)**2)**0.5
    
    def commute(self,nSr,nSc,dr,dc,force):
        if self.a[nSr][nSc]!=0:
            santa_num=self.a[nSr][nSc]
            nnSr,nnSc= nSr+force*dr,nSc+force*dc
            if not self.in_range(nnSr,nnSc):
                self.outSanta+=1
                return
            print(nSr,nSc,dr,dc,force,santa_num,self.M)

            self.a[nnSr][nnSc]=self.a[nSr][nSc]
            self.santa_coord[santa_num]=nnSr,nnSc
            self.is_sleep[santa_num]=True
            self.score[santa_num]+=force

            if self.a[nnSr][nnSc]==0:
                return
            self.commute(nnSr,nnSc,dr,dc,force)

        else:
            return

   
    def roudolf(self):
        dr=[1,0,0,-1,1,1,-1,-1]
        dc=[0,1,-1,0,1,-1,1,-1]
        min_dist=99
        for i in range(8):
            for s in self.santa_coord:
                nRr,nRc=self.Rr+dr[i],self.Rc+dc[i]
                print("santa_coord",self.santa_coord)
                if self.cal_dist(nRr,nRc,s[0],s[1])< min_dist and self.in_range(nRc,nRr):
                    min_dist = self.cal_dist(nRr,nRc,s[0],s[1])
                    dr1,dc1=dr[i],dc[i]
                    santa_num=self.a[s[0]][s[1]]
                    print("nRr,nRc",nRr,nRc)
                    print("santa_num,sr,sc",santa_num,s[0],s[1])
                    print(nRr-s[0],nRc-s[1])
                    print("cal_dist", self.cal_dist(nRr,nRc,s[0],s[1]))
                    

        print("dr1,dc1",dr1,dc1)
        nRr,nRc=self.Rr+dr1,self.Rc+dc1
        print(self.Rr,self.Rc)
        if self.in_range(nRr,nRc):
            print(nRr,nRc)  
            if self.a[nRr][nRc]!=0:
                santa_num=self.a[nRr][nRc]
                print(nRr,nRc,"santa_num2",santa_num)    
                # Sr,Sc=self.santa_coord[santa_num]  
                self.commute(nRr,nRc,dr1,dc1,self.C)
                self.a[nRr][nRc]=0 # 루돌프 이동
        
            self.Rr,self.Rc=nRr,nRc
            print(nRr,nRc)
       

        # self.Sr,self.Sc=self.santa_coord[self.a[nRr][nRc]]

    def santa(self,santa_num):
        Sr,Sc = self.santa_coord[santa_num]
        if self.in_range(Sr,Sc) and self.is_sleep[santa_num]!=True:
            dr=[-1,0,0,1]
            dc=[0,1,-1,0]
            min_dist=self.cal_dist(self.Rr,self.Rc,Sr,Sc)
            for i in range(4):
                nSr,nSc = Sr+dr[i],Sc+dc[i]
                if self.in_range(nSr,nSc) and self.a[nSr][nSc]!=0:
                    if self.cal_dist(self.Rr,self.Rc,nSr,nSc) < min_dist:
                        self.santa_coord[santa_num] = nSr,nSc
                        self.commute(nRr,nRc,Sr,Sc,self.D)
                        self.a[nRr][nRc]= santa_num

                    
if __name__ == "__main__":
    main()