
from email.mime import image 
from secrets import choice
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import TouchRippleBehavior
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.switch import Switch
from kivymd.uix.button import MDRoundFlatButton,MDIconButton,MDTextButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.uix.fitimage import FitImage
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
import time
from kivy.uix.scatter import Scatter
from kivy.logger import Logger
import cv2
from kivy.graphics.vertex_instructions import Quad
from kivy.graphics import *
from kivymd.uix.tab import MDTabs,MDTabsBase
from CANVAS_Project.main import Main as m
from pathlib import Path

import os

KV = """
<RectangleFlatButton>:
    ripple_color: 0, 0, 0, .2
    background_color: 0, 0, 0, 0
    color: root.primary_color

    canvas.before:
        Color:
            rgba: root.primary_color
        Line:
            width: 1
            rectangle: (self.x, self.y, self.width, self.height)
<Main>:
    canvas:
        Color:
            rgba: 0.9764705882352941, 0.9764705882352941, 0.9764705882352941, 1
        Rectangle:
            pos: self.pos
            size: self.size

<Option>:
    canvas:
        Color:
            rgba: 0.9764705882352941, 0.9764705882352941, 0.9764705882352941, 1
        Rectangle:
            pos: self.pos
            size: self.size

<ChoicePart>:
    canvas:
        Color:
            rgba: 0.1, 0.3, 0.2, 1
        Rectangle:
            pos: self.pos
            size: self.size
"""

def get_ratio(img_size, sm_size):
    im_width_ratio = img_size[0] / img_size[1]
    sm_width_ratio = sm_size[0] / sm_size[1]
    if sm_width_ratio>=im_width_ratio: #세로가 먼저 닿을 놈
        w_ratio = (img_size[0]*(sm_size[1]/img_size[1]))/sm_size[0]
        h_ratio = 1
    else : # 가로가 먼저 닿을 놈
        w_ratio = 1
        h_ratio = (img_size[1]*(sm_size[0]/img_size[0]))/sm_size[1]
    return w_ratio,h_ratio
        
    

class RectangleFlatButton(TouchRippleBehavior, Button):
    primary_color = [
        0.12941176470588237,
        0.5882352941176471,
        0.9529411764705882,
        1
    ]

Builder.load_string(KV)

class Main(Screen):                          ## 메인 화면
    #screen= Builder.load_string(KV)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.font='gothic'        ## 메인 화면의 CANVAS 글씨 font
        self.make_main()
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(  ## 이미지 파일 선택하게 해주는 화면을 위한 객체
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )
        
    def make_main(self):                    ## 각 Screen에서 화면의 각 요소 구성 함수
        self.add_widget(
            Label(text='CANVAS',color='blue', pos_hint = {'center_x': 0.5, 'center_y': 0.8},font_size='50',font_name=self.font)
            )

        image_button = RectangleFlatButton(
            text=" Choice a Picture ",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            ripple_color=(0.8, 0.8, 0.8, 0.5),
            )
        image_button.bind(on_press=lambda x:self.file_manager_open(self))
        self.add_widget(image_button)

        b= RectangleFlatButton(
            text="   Take a Picture   ",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            ripple_color=(0.8, 0.8, 0.8, 0.5),
            )

        self.add_widget(b)
        b.bind(on_press=lambda x:self.show_cam())

        a=RectangleFlatButton(
                text="        Option          ",
                pos_hint={"center_x": 0.5, "center_y": 0.3},
                size_hint=(None, None),
                size=(dp(150), dp(50)),
                ripple_color=(0.8, 0.8, 0.8, 0.5),
            )
        self.add_widget(a)
        a.bind(on_press=lambda x:self.show_option())
    
    def show_option(self):                  ## 옵션 키를 눌렀을 시 화면 전환을 위한 함수
        sm.current="option"

    def check_func(self):                   ## 각 핸드폰의 화면의 크기마다 이미지를 fit하고 부분 필터링 체크 여부를 확인하여 각각 알맞게 화면 전환
        print(part_check)
        if(part_check==True):
            sm.current="part_choice"   
            image=Image(source=image_path) #image_path
            im_width_ratio = image.texture_size[0] / image.texture_size[1]
            sm_width_ratio = sm.width / sm.height
            
            if sm_width_ratio>=im_width_ratio: #세로가 먼저 닿을 놈
                w_ratio = (image.texture_size[0]*(sm.height/image.texture_size[1]))/sm.width
                data=FitImage(source=image_path, size_hint_x = w_ratio, size_hint_y = 1, pos_hint = {'center_x': 0.5, 'center_y': 0.5})
            else : # 가로가 먼저 닿을 놈
                h_ratio = (image.texture_size[1]*(sm.width/image.texture_size[0]))/sm.height
                data=FitImage(source=image_path, size_hint_x = 1, size_hint_y = h_ratio, pos_hint = {'center_x': 0.5, 'center_y': 0.5})
            
            sm.current_screen.add_widget(data)
        
        else:
            self.show_choice()
            
    def show_choice(self):                  ## 필터선택 화면2에 대해서 옵션에서 선택 했는지 확인하는 함수
        if(choice2_check==False):
            sm.current="choice"
            takeimage = FitImage(source=image_path,size_hint_y=0.3,size_hint_x=0.3, pos_hint = {'center_x': 0.5, 'center_y': 0.8})
            sm.current_screen.add_widget(takeimage)
        else:                                     
            sm.current="choice2"
            filter_list=["gogh","kimhongdo","oil_paint","cartoon","k_means","in"  ,"bit"]
            for i in list(filter_list):
                m(i,image_path)

    def show_cam(self): ## 카메라를 찍기 위한 화면으로 이동하기 위한 함수
        sm.current="cam"

    def callback_for_menu_items(self, *args): ## 각 필터링을 선택했는지 알려주기 위한 함수
        toast(args[0])

    def file_manager_open(self,a):            ## 파일 매니저에서 이미지를 선택하기 위한 폴더 부분을 정하기 위한 함수
        self.file_manager.show('D:\\capture_picture')  # output manager to the screen
        self.manager_open = True


    def select_path(self, path): #이미지 폴더에서 파일 선택시 호출
        '''It will be called when you click on the file name
        or the catalog selection button.
        
        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.exit_manager()     
        toast(path)
        print(type(path))
        print(path)
        global image_path
        image_path = path
        self.check_func()

        #Choice.show_image(choice)
    
    def exit_manager(self, *args):  ## 파일 매니저를 나가기 위한 함수
        
        self.manager_open = False
        self.file_manager.close()

    
class Option(Screen):               ## Option 화면에 대한 클래스
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.font='gothic'          ## Option 글씨에 대한 font
        self.switch=Switch(
            pos_hint= {'center_x': .7, 'center_y': .6},
            size_hint_y=0.1,
            size_hint_x=0.1
        )
        self.switch1=Switch(
            pos_hint= {'center_x': .7, 'center_y': .3},
            size_hint_y=0.1,
            size_hint_x=0.1
        )
        self.make_option()
    
    def make_option(self):          ## 옵션 화면에 대한 구성 요소를 생성하는 함수
        self.add_widget(
            Label(text='Option',color='blue', pos_hint = {'center_x': 0.5, 'center_y': 0.8},font_size='50',font_name=self.font)
            )

        self.add_widget(
            MDTextButton(
                text=" ALL Train ",
                pos_hint={"center_x": 0.3, "center_y": 0.6},
                size_hint=(None, None),
                size=(dp(150), dp(50)),
                text_color=(0, 1, 0, 1),
            )
        )
        self.add_widget(
            MDTextButton(
                text=" Part Choice ",
                pos_hint={"center_x": 0.3, "center_y": 0.3},
                size_hint=(None, None),
                size=(dp(150), dp(50)),
                text_color=(0, 1, 0, 1),
            )
        )
        print('-----------------------------------')
        print(self.switch)

        self.switch1.bind(active=self.callback)
        self.add_widget(self.switch1)

        self.switch.bind(active=self.callback)
        self.add_widget(self.switch)
        

        back_icon=MDIconButton(
            icon='arrow-left',
            icon_size="30sp",
            pos_hint= {"center_x": .05, "center_y": .95},
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            #md_bg_color:"#ffffff",
            icon_color="#165082"
        )
        
        back_icon.bind(on_press=lambda x:self.show_main())
        self.add_widget(back_icon)

    def show_m(self):               ## 필터 선택 화면2로 이동하기 위한 함수
        sm.current="choice2"

    def callback(self,instance, value):     ## 각 옵션에서 부분필터링 선택 스위치와 필터 선택 화면2 선택 스위치에 대해서 클릭 했을 시 결과 리턴
        if(self.switch == instance):
            print('the switch', instance, 'is', value)
            global choice2_check
            choice2_check = value
            
        elif(self.switch1 == instance):
            global part_check
            part_check = value
            print(part_check)


    def show_main(self):    ## 옵션화면에서 메인 화면으로 가기 위한 함수
        sm.current="main"

class Choice(Screen):       ## 선택화면1에 대한 클래스
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.make_choice()
        self.remove_list=[]
        self.choice_num=None
        self.takeimage=None
        self.takeimage_address=None
    def show_example_list_bottom_sheet(self):       ## 필터 리스트를 보여주기 위한 함수
        bottom_sheet_menu = MDListBottomSheet()
        filter_list=["gogh","kimhongdo","oil_paint","cartoon","k_means","in"  ,"bit"]
        for i in range(len(filter_list)):
            bottom_sheet_menu.add_item(
                f"{filter_list[i]}",
                lambda x, y=i: self.callback_for_menu_items(
                    f"{filter_list[y]}"
                ),
            )

        bottom_sheet_menu.open()

    def callback_for_menu_items(self, *args):       ## 각 필터를 클릭했을 시 이미지 경로와 부분 필터링을 했을 시의 좌표를 이용하여 필터링하는 함수
        toast(args[0])
        global image_path
        image_path = Path(image_path).absolute()
        print(args[0])
        print(image_path)
        global ix,iy,ax,ay
        m(args[0],image_path,ix, ay, ax, iy)# 인수 args[0] : 필터 이름, x:선택 이미지 경로
        sm.current= "preview"
        
        global filter_path
        filter_path = f"./CANVAS_Project/log/{args[0]}.png"
        filter_img = FitImage(source=filter_path, size_hint_y=0.3,size_hint_x=0.3, pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        sm.current_screen.add_widget(filter_img)

    def make_choice(self):                          ## 선택 화면의 각 구성요소를 만들기 위한 함수
        list_bar= MDRoundFlatButton(
            text="  Filter Choice   ",
            icon="palette-outline",                 ## pallette-outline 아이콘 
            icon_size="20sp",
            size_hint=(None, None),
            pos_hint= {"center_x": .5, "center_y": .4},
            size=(dp(150), dp(50)),
            font_size="20sp",
            )
        self.add_widget(list_bar)

        list_bar.bind(on_press=lambda x:self.show_example_list_bottom_sheet())
        
        back_icon=MDIconButton(
            icon='arrow-left',
            icon_size="30sp",
            pos_hint= {"center_x": .05, "center_y": .95},
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            #md_bg_color:"#ffffff",
            icon_color="#165082"
        )
        back_icon.bind(on_press=lambda x:self.show_main())
        self.add_widget(back_icon)

    def show_main(self):                            ## main화면으로 이동하기 위한 함수 각각의 구성요소를 
        sm.current="main"                           ## main화면으로 이동 시 remove_list에 넣어서 삭제 
        for i in range(len(self.remove_list)):      ## 이렇게 하지 않으면 main 갔다가 다시 필터링을 하기 위해 돌아오면 이전 이미지가 그대로 남아있음
            self.remove_widget(self.remove_list[i])
    
    # def show_image(self):
    #     self.takeimage = FitImage(source=image_path, size_hint_y=0.3,size_hint_x=0.3)
    #     self.remove_list.append(self.takeimage)
    #     self.add_widget(self.takeimage)
        
    # def clear(self):
    #     for i in range(len(self.remove_list)):
    #         self.remove_widget(self.remove_list[i])


class Choice2(Screen):                              ## Choice2화면에 대한 클래스
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.make_choice()
        self.d=None
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=Main.exit_manager,
            select_path=Main.select_path,
            preview=True,
        )
        self.remove_list=[]
        self.choice_num=None
        self.takeimage_address=None

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text): ## 각 필터를 나타내는 하나의 tab을 만들어줌
            print(tab_text)
            
            
            img=os.path.join('./CANVAS_Project/log',tab_text+'.png')                    
            if not os.path.isfile(img):
               img=os.path.join('./CANVAS_Project/log',tab_text+'.jpg')
            
            
            screen = Builder.load_string(KV)
            b=Image(source=img,size_hint=(None,None),size=(300,300),pos_hint = {"center_x": .5, "center_y": .5})
            self.d=b
            self.remove_list.append(self.d)
            self.add_widget(b)
            save_btn=MDRoundFlatButton(
            text="      SAVE        ",
            icon="palette-outline",
            icon_size="20sp",
            size_hint=(None, None),
            pos_hint= {"center_x": .5, "center_y": .2},
            size=(dp(150), dp(50)),
            font_size="20sp")
            self.add_widget(save_btn)
            save_btn.bind(on_press=lambda x:self.image_save(img)) 
            # 이미지 띄우는거 가운데 사이즈 choice1 처럼
            #버튼 하나만 저장 
            
    def image_save(self,image_name): # 이미지 저장
      t=time.time()
      t=str(int(round(t,0)))
      data=cv2.imread(image_name)
      path1=os.path.join('./gallery',f'{t}.png')
      print(path1)
      cv2.imwrite(path1,data)
      toast('SAVE')

    def make_choice(self, *args):           ## choice 화면을 구성하는 요소들을 만드는 함수
        # filter_list=["Gogh","Kim hong do","Oil paint","Cartoon","Custom"]
        filter_list=["gogh","kimhongdo","oil_paint","cartoon","k_means","in"  ,"bit"]
        tab=MDTabs()
        for i in range(len(filter_list)):
          i=MDTabsBase(title=filter_list[i])
          tab.add_widget(i)
        self.add_widget(tab)
        tab.bind(on_tab_switch=lambda a,b,c,d:self.on_tab_switch(a,b,c,d))
        back_icon=MDIconButton(
                icon='arrow-left',
                icon_size="30sp",
                pos_hint= {"center_x": .05, "center_y": .87},
                size_hint=(None, None),
                size=(dp(150), dp(50)),
                #md_bg_color:"#ffffff",
                icon_color="#165082"
            )
        back_icon.bind(on_press=lambda x:self.show_main())
        self.add_widget(back_icon)
        
    def show_main(self):                    ## main 함수로 이동하는 함수 각각의 remove_list로 이전 요소들 삭제
      sm.current="main"
      for i in range(len(self.remove_list)):
          self.remove_widget(self.remove_list[i])

class Cam(Camera):                          ## 카메라를 만들기 위한 클래스
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size=(300,300)
        self.resolution=(640,480)
        self.allow_stretch=True
        self.play=True

class CamScreen(Screen):                    ## 만든 카메라를 하나의 화면으로 만들기 위한 클래스
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cam=Cam()
        self.add_widget(self.cam)
        self.capture_button=MDIconButton(icon="camera",icon_size='30sp',
                                        pos_hint= {"center_x": .5, "center_y": .1},
                                        size_hint=(None, None),
                                        md_bg_color="white",
                                        size=(dp(150), dp(50)))

        self.add_widget(self.capture_button)
        self.capture_button.bind(on_press=lambda x:self.capture())
        # self.back_icon=MDIconButton(
        #     icon='arrow-left',
        #     icon_size="30sp",
        #     pos_hint= {"center_x": .05, "center_y": .95},
        #     size_hint=(None, None),
        #     size=(dp(150), dp(50)),
        #     #md_bg_color:"#ffffff",
        #     icon_color="#165082"
        # )
        # self.add_widget(self.back_icon)

    def capture(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        data=self.cam.export_as_image("photo_{}.png".format(timestr))
        data.save("photo_{}.jpg".format(timestr))
        self.address="photo_{}.jpg".format(timestr)
        global image_path
        image_path= self.address="photo_{}.jpg".format(timestr)
        toast("wait...")
        if(part_check==True):
            
            sm.current="part_choice"   
            image=Image(source=image_path) #image_path

            w_ratio, h_ratio= get_ratio((image.texture_size[0], image.texture_size[1]), (sm.width, sm.height))
            data=FitImage(source=image_path, size_hint_x = w_ratio, size_hint_y = h_ratio, pos_hint = {'center_x': 0.5, 'center_y': 0.5})
            sm.current_screen.add_widget(data)

        else:
            
            self.show_choice(timestr)
        
        # else:
        #     sm.current_screen.add_widget(data)
        # # self.show_choice(timestr)
    def show_choice(self,timestr):
        if(choice2_check==False):
            sm.current="choice" 
            image_path="./photo_{}.jpg".format(timestr)    
            self.takeimage = FitImage(source=image_path, size_hint_y=0.3,size_hint_x=0.3, pos_hint = {'center_x': 0.5, 'center_y': 0.8})
            sm.current_screen.add_widget(self.takeimage)   
        else:
            sm.current="choice2"
            filter_list=["gogh","kimhongdo","oil_paint","cartoon","k_means","in"  ,"bit"]
            for i in list(filter_list):
                m(i,image_path)

class ChoicePart(Screen):   
    def __init__(self, **kwargs):   
        super().__init__(**kwargs)  
        self.point_l=[] 
        self.check=0 

    def on_touch_down(self, touch): 
        if super(ChoicePart, self).on_touch_down(touch):    
            return True 
        Logger.info('tesselate: on_touch_down (%5.2f, %5.2f)' % touch.pos)      

        if(len(self.point_l)<2):    
            self.point_l.append(touch.pos)

        if(len(self.point_l)==2):
            # sm.current_screen.canvas.add(Rectangle(points=[self.point_l[0][0],self.point_l[0][1],
            #                                             self.point_l[1][0],self.point_l[0][1],
            #                                             self.point_l[1][0],self.point_l[1][1],
            #                                             self.point_l[0][0],self.point_l[0][1]]))
            min_x = min(self.point_l[1][0], self.point_l[0][0])
            max_x = max(self.point_l[1][0], self.point_l[0][0])
            min_y = min(self.point_l[1][1], self.point_l[0][1])
            max_y = max(self.point_l[1][1], self.point_l[0][1])

            width=abs(self.point_l[1][0]-self.point_l[0][0])
            height=abs(self.point_l[1][1] - self.point_l[0][1])
            
            sm.current_screen.canvas.add(Line(rectangle=(min_x, min_y,width,height),width=3))
            
            global image_path
            global ix,ax,iy,ay
            
            ix=0
            ax=0
            iy=0
            ay=0

            a=cv2.imread(image_path)
            all_x,all_y,c =a.shape

            w_ratio, h_ratio = get_ratio((all_y,all_x),(sm.width,sm.height))

            if w_ratio == 1 and h_ratio != 1:
                img_width = int(sm.width)
                img_height = int(sm.height * h_ratio)
                img_start_y = int(sm.height*(1-h_ratio)/2)
                min_y, max_y = min_y-img_start_y, max_y-img_start_y
            
            elif w_ratio != 1 and h_ratio == 1 :
                img_width = int(sm.width * w_ratio)
                img_height = int(sm.height)
                img_start_x = int(sm.width*(1-w_ratio)/2)
                min_x, max_x = min_x-img_start_x, max_x-img_start_x
            
            else :
                img_width = int(sm.width * w_ratio)
                img_height = int(sm.height)
                img_start_x = int(sm.width*(1-w_ratio)/2)
                min_x, max_x = min_x-img_start_x, max_x-img_start_x
            
            x_trans = lambda x : int(x*(all_y/img_width))
            y_trans = lambda y : int(y*(all_x/img_height))
            min_x,max_x,min_y,max_y = x_trans(min_x),x_trans(max_x),y_trans(min_y),y_trans(max_y)
            
            min_x = min_x * (500/all_y)
            max_x = max_x * (500/all_y)
            min_y = 500-min_y * (500/all_x)
            max_y = 500-max_y * (500/all_x)

            
            if(choice2_check==False):
                self.point_l=[]
                takeimage = FitImage(source=image_path, size_hint_y=0.3,size_hint_x=0.3, pos_hint = {'center_x': 0.5, 'center_y': 0.8})
                sm.current='choice'
                sm.current_screen.add_widget(takeimage)
                ix=min_x
                ax=max_x
                iy=min_y
                ay=max_y

            else:
                self.point_l=[]
                sm.current="choice2"
                filter_list=["gogh","kimhongdo","oil_paint","cartoon","k_means","in"  ,"bit"]
                for i in list(filter_list):
                    m(i,image_path,min_x,max_y,max_x,min_y)

##########미리보기 화면###########
# 버튼은 전부 구현 함
# 화면에 이미지 나오는것은 구현 아직 안함
# 실행 안해봄
# home버튼 클릭시 이미지 작동 잘하는지 모르겠음
# 하기 싫다
# 집가고 싶음

class Preview(Screen):
  def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.make_preview()
        self.remove_list=[]
        self.choice_num=None
        self.takeimage=None
        self.takeimage_address=None
  def make_preview(self):
    home_icon=MDIconButton(
            icon='home',
            icon_size="30sp",
            pos_hint= {"center_x": .05, "center_y": .95},
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            #md_bg_color:"#ffffff",
            icon_color="#165082"
        )
    home_icon.bind(on_press=lambda x:self.show_main())
    self.add_widget(home_icon)
    save_btn=MDRoundFlatButton(
        text="      SAVE        ",
        icon="palette-outline",
        icon_size="20sp",
        size_hint=(None, None),
        pos_hint= {"center_x": .5, "center_y": .2},
        size=(dp(150), dp(50)),
        font_size="20sp")
    self.add_widget(save_btn)
    global filter_path
    save_btn.bind(on_press=lambda x:self.image_save(filter_path))# 이미지 경로 입력
  def image_save(self,image_name): # 이미지 저장
      t=time.time()
      t=str(int(round(t,0)))
      data=cv2.imread(image_name)
      path1=os.path.join('./gallery',f'{t}.png')
      print(path1)
      cv2.imwrite(path1,data)
      toast('save')
      
  def show_main(self):
      sm.current="main"
      for i in range(len(self.remove_list)):
          self.remove_widget(self.remove_list[i])

class TutorialApp(MDApp):
    def build(self):
        global sm
        sm=ScreenManager()
        global choice2_check
        choice2_check = False
        global part_check
        part_check = False
        global image_path
        image_path=''
        global ix,iy,ax,ay
        ix=0
        iy=0
        ax=0
        ay=0
        sm.add_widget(Main(name="main"))
        sm.add_widget(Option(name="option"))
        sm.add_widget(Choice(name="choice"))
        sm.add_widget(CamScreen(name='cam'))
        sm.add_widget(Choice2(name="choice2"))
        sm.add_widget(ChoicePart(name="part_choice"))
        sm.add_widget(Preview(name="preview"))
        return sm

if __name__ == "__main__":
    TutorialApp().run()
    