"""
跨屏图像检测与自动点击工具

功能逻辑：
1. 每 60 秒截取所有显示器（双屏或多屏）的完整画面。
2. 在截图中寻找 Auto-fill.jpg，找到后点击其中心。
3. 再次截图，寻找 Combine.jpg，找到后点击；若未找到，则检查是否存在 NothingToCombine.jpg。
4. 若存在 NothingToCombine.jpg，则寻找 combine_re.jpg 并点击。
5. 每次循环结束，鼠标移到虚拟桌面中心。

退出方式：按下 Ctrl+Esc 全局热键，程序安全退出。
"""

import os
import time
from symtable import Function

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import keyboard  # 用于监听全局热键

# ================== 可自定义的全局参数 ==================
CHECK_INTERVAL = 600          # 检测间隔（秒）
MATCH_THRESHOLD = 0.8        # 图像匹配阈值，范围 0~1，越高要求越严格

# 模板图片文件名（务必与脚本放在同一目录）
AUTOFILL_IMG = "Auto-fill.jpg"
COMBINE_IMG = "Combine.jpg"
NOTHING_IMG = "NothingToCombine.jpg"
COMBINE_RE_IMG = "combine_re.jpg"
ACCESSORIES_IMG = "Accessories.jpg"
EQUIPMENT_IMG = "Equipment.jpg"
MATERIALS_IMG = "Materials.jpg"
MORE_IMG = "More.jpg"
MAKE_IMG = "make.jpg"
MAKING_IMG = "making.jpg"
TAP_IMG = "tap.jpg"
FUNCTIONS_IMG = "Function.jpg"
RING_IMG = "Ring.jpg"
MAGIC_IMG = "magic.jpg"


# =====================================================

pyautogui.FAILSAFE = False   # 关闭故障安全保护，允许鼠标移动到屏幕任意角落

# 全局退出标志，当热键触发时置为 True，主循环检测到后退出
EXIT_FLAG = False


def set_exit_flag():
    """
    Ctrl+Esc 热键的回调函数。
    作用：将全局变量 EXIT_FLAG 设为 True，通知主循环安全退出。
    无参数，无返回值。
    """
    global EXIT_FLAG
    print("\n检测到 Ctrl+Esc，正在安全退出程序...")
    EXIT_FLAG = True


def load_image(path):
    """
    加载并返回模板图片，如果文件不存在则抛出异常。

    参数:
        path (str): 图片文件的完整路径。

    返回:
        numpy.ndarray: OpenCV 格式的彩色图像（BGR 顺序）。

    异常:
        FileNotFoundError: 当指定路径的文件不存在时抛出。
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"缺少必要图片：{path}，请放入脚本同目录")
    # imread 以彩色方式读取，保持颜色信息用于准确匹配
    return cv2.imread(path, cv2.IMREAD_COLOR)


def capture_full_screen():
    """
    截取所有显示器组成的虚拟桌面画面。
    无论用户使用单屏、双屏还是多屏，返回的都是一张包含所有屏幕的完整截图。

    返回:
        numpy.ndarray: 整个虚拟桌面的截图，格式为 BGR 彩色图像。
    """
    # ImageGrab.grab(all_screens=True) 可一次性抓取整个虚拟桌面
    screenshot = ImageGrab.grab(all_screens=True)
    # PIL 默认使用 RGB 顺序，OpenCV 使用 BGR，因此需要转换
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def find_template(template, threshold=MATCH_THRESHOLD):
    """
    在屏幕截图中寻找指定的模板图片。
    使用 OpenCV 的模板匹配算法，采用归一化相关系数法，
    返回匹配度最高且超过阈值的位置信息。

    参数:
        screen_img (numpy.ndarray): 完整的屏幕截图（BGR 图像）。
        template   (numpy.ndarray): 要搜索的模板图片（BGR 图像）。
        threshold  (float): 匹配相似度阈值（0~1），默认使用全局参数 MATCH_THRESHOLD。

    返回:
        tuple: (max_val, max_loc, center)
            - max_val (float): 最佳匹配的相似度值（0~1）。
            - max_loc (tuple): 最佳匹配区域左上角坐标 (x, y)，未找到时为 None。
            - center  (tuple): 最佳匹配区域的中心点坐标 (x, y)，可直接用于鼠标操作，未找到时为 None
    """
    screen_img = capture_full_screen()
    # TM_CCOEFF_NORMED 归一化相关系数，值越接近 1 说明越相似
    result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
    # 获取整个结果矩阵中的最大值、最小值及其位置
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # 如果相似度达到要求，计算模板中心点在屏幕中的绝对坐标
    if max_val >= threshold:
        h, w = template.shape[:2]           # 模板的高度和宽度
        center_x = max_loc[0] + w // 2      # 左上角 x + 宽度的一半
        center_y = max_loc[1] + h // 2      # 左上角 y + 高度的一半
        return max_val, max_loc, (center_x, center_y)

    # 未找到时返回默认值
    return 0, None, None


def move_and_click(center, desc=""):
    """
    移动鼠标到指定坐标，并执行一次左键单击。
    如果坐标为 None，则直接返回不执行任何操作。

    参数:
        center (tuple): 目标坐标 (x, y)。
        desc   (str): 操作描述，用于日志输出。
    """
    if center is None:
        return
    # 将鼠标平滑移动到目标位置，duration=0.1 使移动在 0.1 秒内完成
    pyautogui.moveTo(center[0], center[1], duration=0.1)
    # 执行鼠标左键单击
    pyautogui.click()
    print(f"  -> 点击 {desc} 位置：{center}")

def combineEquipment():
    # 处理装备的逻辑
    tpl_more = load_image(MORE_IMG)
    tpl_auto = load_image(AUTOFILL_IMG)
    tpl_combine = load_image(COMBINE_IMG)
    tpl_Equipment = load_image(EQUIPMENT_IMG)
    tpl_combine_re = load_image(COMBINE_RE_IMG)

    pyautogui.press('space')
    val, _, center_more = find_template(tpl_more)
    if center_more is not None:
        move_and_click(center_more, "tpl_more")

    val, _, center_Equipment = find_template(tpl_Equipment)
    if center_Equipment is not None:
        move_and_click(center_Equipment, "tpl_Equipment")

    val, _, center_auto = find_template(tpl_auto)
    if center_auto is not None:
        move_and_click(center_auto, "auto")

    val, _, center_combine = find_template(tpl_combine)
    if center_combine is not None:
        move_and_click(center_combine, "combine")

    val, _, center_combine_re = find_template(tpl_combine_re)
    if center_combine_re is not None:
        move_and_click(center_combine_re, "combine_re")

def combineMaterials():
    # 处理材料的逻辑
    tpl_more = load_image(MORE_IMG)
    tpl_auto = load_image(AUTOFILL_IMG)
    tpl_combine = load_image(COMBINE_IMG)
    tpl_Materials = load_image(MATERIALS_IMG)
    tpl_combine_re = load_image(COMBINE_RE_IMG)

    pyautogui.press('space')
    val, _, center_more = find_template(tpl_more)
    if center_more is not None:
        move_and_click(center_more, "tpl_more")

    val, _, center_Materials = find_template(tpl_Materials)
    if center_Materials is not None:
        move_and_click(center_Materials, "tpl_Materials")

    val, _, center_auto = find_template(tpl_auto)
    if center_auto is not None:
        move_and_click(center_auto, "auto")

    val, _, center_combine = find_template(tpl_combine)
    if center_combine is not None:
        move_and_click(center_combine, "combine")

    val, _, center_combine_re = find_template(tpl_combine_re)
    if center_combine_re is not None:
        move_and_click(center_combine_re, "combine_re")

def Level80Ring():
    tpl_make = load_image(MAKE_IMG)
    tpl_making = load_image(MAKING_IMG)
    tpl_tap = load_image(TAP_IMG)
    tpl_function = load_image(FUNCTIONS_IMG)
    tpl_ring = load_image(RING_IMG)
    tpl_magic = load_image(MAGIC_IMG)
    tpl_auto = load_image(AUTOFILL_IMG)

    val, _, center_tap = find_template(tpl_tap)
    if center_tap is not None:
        move_and_click(center_tap, "center_tap")
    pyautogui.press('space')
    val, _, center_magic = find_template(tpl_magic)
    if center_magic is not None:
        move_and_click(center_magic, "center_magic")

    val, _, center_function = find_template(tpl_function)
    if center_function is not None:
        print("1111")
        move_and_click(center_magic, "center_function")

    val, _, center_make = find_template(tpl_make)
    if center_make is not None:
        move_and_click(center_magic, "center_make")

    val, _, center_ring = find_template(tpl_ring)
    if center_ring is not None:
        move_and_click(center_magic, "center_ring")

    val, _, center_auto = find_template(tpl_auto)
    if center_auto is not None:
        move_and_click(center_magic, "center_auto")

    val, _, center_makeing = find_template(tpl_making)
    if center_makeing is not None:
        move_and_click(center_magic, "center_makeing")


def openMagic():
    tpl_magic = load_image(MAGIC_IMG)
    tpl_tap = load_image(TAP_IMG)
    val, _, center_tap = find_template(tpl_tap)
    if center_tap is not None:
        move_and_click(center_tap, "center_tap")
    pyautogui.press('space')
    val, _, center_magic = find_template(tpl_magic)
    if center_magic is not None:
        move_and_click(center_magic, "center_magic")

def closeMagic():
    tpl_magic = load_image(MAGIC_IMG)
    tpl_tap = load_image(TAP_IMG)
    val, _, center_tap = find_template(tpl_tap)
    if center_tap is not None:
        move_and_click(center_tap, "center_tap")


def main():
    """
    主函数，负责初始化、循环检测和退出控制。
    """
    global EXIT_FLAG

    # ---- 注册全局热键 Ctrl+Esc，绑定回调函数 ----
    keyboard.add_hotkey("ctrl+esc", set_exit_flag)

    print("程序已启动，每600秒检测一次（支持双屏/多屏）")
    print("按 Ctrl+Esc 停止程序")

    # ---- 主循环：只要退出标志未置位，就持续运行 ----
    while not EXIT_FLAG:
        openMagic()
        combineEquipment()
        time.sleep(2)
        combineMaterials()
        time.sleep(2)
        closeMagic()
        # Level80Ring()
        # 无论是否匹配成功，都将鼠标移回整个虚拟桌面的中心
        screen = capture_full_screen()
        h, w = screen.shape[:2]           # 虚拟桌面的高度和宽度
        center_all = (w // 2, h // 2)      # 中心点坐标
        pyautogui.moveTo(center_all[0], center_all[1], duration=0.1)
        print(f"  鼠标已移至总屏幕中心：{center_all}")

        # 7. 分段等待检测间隔，这样能及时响应退出热键
        for _ in range(CHECK_INTERVAL):
            if EXIT_FLAG:
                break
            time.sleep(1)

    print("程序已退出。")


if __name__ == "__main__":
    main()