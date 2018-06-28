#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Tkinter
import tkMessageBox
import codecs
import time

############################################################################

# 여기에 한양인 포털 아이디와 비밀번호를 적어주세요
YOUR_PORTAL_ID = 'tlsgusghq'
YOUR_PORTAL_PW = 'khs0202713'

# 자동 수강하고 싶은 강의가 강의실에서 몇 번째 항목인지 설정합니다. 기본적으로 교양강의를 듣지 않을경우 HELP는 첫번째에 있습니다.
LECTURE_ORDER = 5

# Chrome Driver 사이트에서 받은 ChromeDriver.exe 파일의 경로를 지정해주시면 됩니다.
CHROME_DRIVER_PATH = '/Users/Tanukimong/Python/ChromeDriver/chromedriver'

# 페이지 간의 이동 대기시간을 설정합니다. 인터넷 속도가 느리거나 지속적으로 오류가 발생한다면 이 값을 늘려보세요(3-5 권장).
SLEEP_TIME = 3

# 페이지 내의 이동 대기시간을 설정합니다. 인터넷 속도가 느리거나 지속적으로 오류가 발생한다면 이 값을 늘려보세요(1-2 권장).
SLEEP_SHORTTIME = 1

# 총 강의 페이지를 설정합니다(강의실에서 아래에 적혀있는 1 2 3 4 5 6페이지)
LECTUREROOM_PAGE = 7

# 온라인 강의의 페이지 최댓값을 설정합니다(온라인 강의 플레이어에서 좌우로 넘길 수 있는 페이지 수).
LECTURE_PAGE = 50

# 강의실에서 대기할 시간을 설정합니다(단위 : 분). (HELP의 경우 30분, 과기철의 경우 6-70분 권장)
LECTURE_TIME = 65

# Chrome 창을 숨길 지 설정합니다. True로 설정하여 숨길 수 있습니다. 실수로 다른 브라우저로 포털에 들어갈 경우 자동 수강은 끊기기 때문에 False로 설정하는 것을 권장합니다.
HEADLESS_MODE = False

WINDOW_RESOULTION = '2560x1600'#맥북 해상도

############################################################################

if YOUR_PORTAL_ID == '' or YOUR_PORTAL_PW=='':
	tkMessageBox.showinfo(unicode('정보 입력', 'utf-8'), unicode('유저 정보를 입력해주세요.', 'utf-8'))

# Headless로 Chrome 시동
options = webdriver.ChromeOptions()

if HEADLESS_MODE :
	options.add_argument('headless')
options.add_argument('window-size=' + WINDOW_RESOULTION)
#options.add_argument("--disable-gpu")

driver = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=options)

# 포털 로그인페이지 로딩
driver.get('https://portal.hanyang.ac.kr/sso/lgin.do')

# ID와 PW를 입력
driver.find_element_by_name('userId').send_keys(YOUR_PORTAL_ID)
driver.find_element_by_name('password').send_keys(YOUR_PORTAL_PW)

# 로그인 버튼을 누름
lginBtn = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, '//fieldset/p[3]/a')))

lginBtn.send_keys('\n')

# 비밀번호 변경 안내문 넘기기
try :
	skipButton = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, '//span[@class="input_ btn_common_wrap btn_white_wrap btn_medium_wrap"]/input')))
	skipButton.click()
except:
	# 안내문이 열리지않음 = 보안개념이 철저하시군요.
	print 'Alert Skipped.'

# 포털 메인페이지 로드
time.sleep(SLEEP_TIME)

# 강의실 버튼을 누름
classRoomBtn = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/p')))
classRoomBtn.click()

# 수업 목록 table을 얻어옴
table_xpath = '//*[@id="ilbanGangjwaStud"]'
tbody_xpath = table_xpath + '/tbody/'

# HELP 강의실로 이동
goto_classHome = tbody_xpath + '/tr[' + str(LECTURE_ORDER) + ']/td[9]/span/input'
goto_classHome = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, goto_classHome)))
goto_classHome.send_keys('\n')

# 연구실 안전교육 이수 알림창 닫기
try :
	alert = WebDriverWait(driver, SLEEP_TIME).until(EC.alert_is_present())
	alert.dismiss()
except:
	# 알림창이 열리지않음 = 이수완료. 성실하시군요
	print 'Alert Skipped.'

# 강의홈 로딩
time.sleep(SLEEP_TIME)
driver.switch_to_window(driver.window_handles[1])

# 좌측 강의 버튼 누르기
goto_lecturePage = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, '//li[1]/span/a')))
goto_lecturePage.send_keys('\n')

for page_count in range(1, LECTUREROOM_PAGE + 1):

	# 페이지 이동
	driver.execute_script('javascript:fncList("'+ str(page_count) +'");')

	# 페이지 안에서 온라인 강의가 없는 항목의 개수
	skip_count = 0

	for lecture_count in range(1, 4):

		# 1/3 강의 확인

		try:
			lecture_Progress = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="fl_l wp_70"])[' + str(lecture_count) + ']/dl/dd[3]/span[3]')))
		except:
			skip_count =  skip_count + 1
			continue;

		print lecture_Progress.text

		# 자동 수강.
		if lecture_Progress.text != '(100%)':
			# 해당 회차 열기

			print lecture_count - skip_count

			open_lectureWindow = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, '(//a[@class="lectureWindow"])[' + str(lecture_count - skip_count) + ']')))
			open_lectureWindow.click()

			# 강의창 확인
			time.sleep(SLEEP_TIME)
			driver.switch_to_window(driver.window_handles[2])

			# 우선 끝까지 넘김
			navi_nextButton = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, '//a[@id="btn_next"]')))

			for click_count in range(1, LECTURE_PAGE + 1):
				navi_nextButton = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, '//a[@id="btn_next"]'))).send_keys('\n')

			# 강의가 끝날때까지 대기
			for i in range(0, LECTURE_TIME * 6 + 3):
				# 10초 대기. 단, 아래에 SLEEP_TIME 6초 대기가 있으므로 그만큼 빼줌.
				time.sleep(10 - 2 * SLEEP_TIME)

				# 1차적으로 JS로 경고창을 해제
				driver.execute_script('window.onbeforeunload = function(e){};')

				# 새로고침하여 세션 유지
				driver.refresh()

				# 그래도 뜰 경우를 대비해 '페이지를 나가시겠습니까?' 경고창 대기
				time.sleep(SLEEP_TIME)

				print 'Lecture wait.. ', i, '/', LECTURE_TIME * 6 + 3

				# '페이지를 나가시겠습니까?' 경고창 닫기
				try :
					alert = WebDriverWait(driver, SLEEP_TIME).until(EC.alert_is_present())
					alert.accept()
				except:
					# 알림창이 열리지않음 = 다행히도 해제됐군요
					continue

			# 1차적으로 JS로 경고창을 해제
			driver.execute_script('window.onbeforeunload = function(e){};')

			# 강의창 닫아줌
			navi_closeButton = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, '//a[@id="close_lectureWindow"]')))
			navi_closeButton.click()

			# 그래도 뜰 경우를 대비해 '페이지를 나가시겠습니까?' 경고창 대기
			time.sleep(SLEEP_TIME)

			# '페이지를 나가시겠습니까?' 경고창 닫기
			try :
				alert = WebDriverWait(driver, SLEEP_TIME).until(EC.alert_is_present())
				alert.accept()
			except:
				# 알림창이 열리지않음 = 다행히도 해제됐군요
				print 'Alert Skipped.'

			# 원래 강의실로 돌아감
			driver.switch_to_window(driver.window_handles[1])

	time.sleep(SLEEP_SHORTTIME)

tkMessageBox.showinfo(unicode('드디어 다 들었닭!', 'utf-8'), unicode('오늘 저녁은 치킨이닭!', 'utf-8'))
driver.quit()
