import random
import re

class Random_baseball:
    
    def __init__(self):
        self.ran_list=[]
        self.count=1
        while len(self.ran_list)<3:
            ran_number=random.randrange(1,10)
            if ran_number not in self.ran_list:
                self.ran_list.append(ran_number)
            else:
                pass

        # self.match_number()
        
    def input_number(self):
        nums=[]
        
        
        regex=re.compile('\d')
        tt=input("숫자입력 : ")
        input_num=regex.findall(tt)
        
        if tt=='q':
            print(self.help_info())
            self.exit_game()
            
        if len(input_num)==int(3):
            for x in input_num:
                if x.isdigit()==False:
                    print("숫자를 입력해주세요.")
                    continue
                x=int(x)
                if x > 9:
                    print("0~9까지 숫자만 입력해주세요.")
                    continue
                if x in nums:
                    print('이미 입력한 숫자입니다.')
                    continue
                nums.append(x)
        else:
            print("3개의 숫자를 연달아 입력하세요!")
            self.match_number()

        return nums

    def match_number(self):
        strike_number = 0
        ball_number = 0
        
        input_list=self.input_number()
        
        for idx, num in enumerate(input_list):
            if num == self.ran_list[idx]:
                strike_number += 1
            else:
                if num in self.ran_list:
                    ball_number += 1
                else:
                    pass
            
        print(f'입력한 숫자 : {input_list}')
        print(self.ran_list)
        if strike_number == 0 and ball_number == 0:
            print("OUT")
        else:
            print(f"{strike_number}STRIKE {ball_number}BALL")
        if self.ran_list==input_list:
            print(self.ran_list)
            self.win()
            return
        self.count+=1
        self.match_number()

    def exit_game(self):
        quit_game=input("게임에서 나가시겠습니까?\n[y/n] : ")
        if quit_game=="y":
            quit()

        elif quit_game=="n":
            self.match_number()

        else:
            print("-----------------------------\ny 또는 n으로 입력해주세요!\n-----------------------------")
            self.exit_game()

    def win(self):
        print(f"{self.count}번 만에 맞혔습니다.")
        quit()

    def search_index(self,num):
        if num in self.ran_list:
            index_num=self.ran_list.index(num)
        return index_num

    def help_info(self):
        return"""
        -------------------------------------------------------------------------------
        숫자를 연달아 입력하여 맞히는 숫자야구게임입니다. 1~9까지 연달아 숫자를 입력해주세요!
        게임을 나가고 싶으면 'q'를 입력해주세요!
        -------------------------------------------------------------------------------
        """

def main():
    
    bs=Random_baseball()
    print(bs.help_info())
    bs.match_number()
    
if __name__ == "__main__":
    main()        

            

