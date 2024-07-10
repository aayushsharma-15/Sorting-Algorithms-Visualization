import pygame
import random

pygame.font.init()
pygame.init()

W = 980
H = 750
sortpoint = 0
sort = 'merge'
surf = pygame.display.set_mode((W, H))
run = True

NUM_BARS = 20
MAX_HEIGHT = 50
BAR_WIDTH = 10
GAP = 4
BUTTON_HEIGHT = 50
BUTTON_Y_POS = H - 100
l1 = [0 for _ in range(NUM_BARS)]
blank = [(255, 255, 255) for _ in range(NUM_BARS)]
anim_color = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
f = pygame.font.SysFont("comicsans", 30)

# Initialize the grid with random values
def draw_grid():
    for x in range(NUM_BARS):
        blank[x] = anim_color[0]
        l1[x] = random.randrange(1, MAX_HEIGHT)
draw_grid()

# Redraw window function
def redrawWindow():
    surf.fill((0, 0, 0))
    draw()
    draw_buttons()
    pygame.display.update()
    pygame.time.delay(30)

# Draw the grid and text
def draw():
    global sort
    text = f.render("Sorting Analyzer", 1, (255, 255, 255))
    surf.blit(text, (10, 20))
    t = "{} sort".format(sort)
    text = f.render(t, 1, (255, 255, 255))
    surf.blit(text, (W - 300, 45))
    barW = (W - 50) // NUM_BARS
    boundary_l1 = (W - 100) / NUM_BARS
    boundary_grp = (BUTTON_Y_POS - 100) / MAX_HEIGHT  # Adjusted for button spacing
    pygame.draw.line(surf, (255, 255, 255), (42, 95), (950, 95), 6)
    for x in range(1, MAX_HEIGHT):
        pygame.draw.line(surf, (0, 0, 0), (42, boundary_grp * x + 100), (900, boundary_grp * x + 100), 1)
    for x in range(NUM_BARS):
        # Draw border
        pygame.draw.rect(surf, (0, 0, 0), (boundary_l1 * x - 3 + 42, 100, barW, l1[x] * boundary_grp))
        # Draw inner bar with a gap
        pygame.draw.rect(surf, blank[x], (boundary_l1 * x - 3 + 42 + 2, 100 + 2, barW - 4, l1[x] * boundary_grp - 4))

# Draw buttons function
def draw_buttons():
    buttons = ["New Array", "Sort", "Change"]
    text_rects = []
    button_width = 150
    button_height = BUTTON_HEIGHT
    for i, button in enumerate(buttons):
        button_rect = pygame.Rect(W // 4 * (i + 1) - button_width // 2, BUTTON_Y_POS, button_width, button_height)
        pygame.draw.rect(surf, (255, 255, 255), button_rect)  # Yellow button
        text = f.render(button, 1, (0, 0, 0))  # Black text
        text_rect = text.get_rect(center=button_rect.center)
        surf.blit(text, text_rect)
        text_rects.append(button_rect)

# Merge sort algorithm
def merge_sort(l1, l, r):
    midpoint = (l + r) // 2
    if l < r:
        merge_sort(l1, l, midpoint)
        merge_sort(l1, midpoint + 1, r)
        merge(l1, l, midpoint, midpoint + 1, r)

def merge(l1, x1, y1, x2, y2):
    temp = []
    q = x1
    w = x2
    while q <= y1 and w <= y2:
        blank[q] = anim_color[1]
        blank[w] = anim_color[1]
        redrawWindow()
        blank[q] = anim_color[0]
        blank[w] = anim_color[0]
        if l1[q] < l1[w]:
            temp.append(l1[q])
            q += 1
        else:
            temp.append(l1[w])
            w += 1
    while q <= y1:
        blank[q] = anim_color[1]
        redrawWindow()
        blank[q] = anim_color[0]
        temp.append(l1[q])
        q += 1
    while w <= y2:
        blank[w] = anim_color[1]
        redrawWindow()
        blank[w] = anim_color[0]
        temp.append(l1[w])
        w += 1
    w = 0
    for q in range(x1, y2 + 1):
        pygame.event.pump()
        if w < len(temp):
            l1[q] = temp[w]
            w += 1
            blank[q] = anim_color[3]
            redrawWindow()
            blank[q] = anim_color[3]

# Bubble sort algorithm
def bubble_sort(nums):
    i = 0
    numslen = len(nums)
    fl = True
    while i < numslen and fl:
        fl = False
        for l in range(numslen - i - 1):
            if nums[l] > nums[l + 1]:
                pygame.event.pump()
                t = nums[l]
                nums[l] = nums[l + 1]
                nums[l + 1] = t
                blank[l] = anim_color[1]
                redrawWindow()
                blank[l] = anim_color[3]
                fl = True
        i += 1

# Insertion sort algorithm
def insertion_sort(nums):
    numslen = len(nums)
    for i in range(numslen):
        pygame.event.pump()
        cv = nums[i]
        blank[i] = anim_color[1]
        redrawWindow()
        blank[i] = anim_color[0]
        p = i
        while p > 0 and nums[p - 1] > cv:
            nums[p] = nums[p - 1]
            p -= 1
        nums[p] = cv
        blank[p] = anim_color[1]
        redrawWindow()
        blank[p] = anim_color[3]

# Quick sort algorithm
def partition(nums, start, end):
    pivot = nums[start]
    blank[pivot] = anim_color[2]
    lm = start + 1
    rm = end
    done = False
    while not done:
        pygame.event.pump()
        blank[pivot] = anim_color[2]
        while lm <= rm and nums[lm] <= pivot:
            lm += 1
            if lm <= end:
                blank[lm] = anim_color[1]
                redrawWindow()
                blank[lm] = anim_color[0]
        while nums[rm] >= pivot and rm >= lm:
            rm -= 1
            if rm >= start:
                blank[rm] = anim_color[1]
                redrawWindow()
                blank[rm] = anim_color[0]
        if rm < lm:
            done = True
        else:
            temp = nums[lm]
            nums[lm] = nums[rm]
            nums[rm] = temp
    
    temp = nums[start]
    nums[start] = nums[rm]
    nums[rm] = temp
    return rm

def quick_sort(nums, start, end):
    if start < end:
        split = partition(nums, start, end)
        quick_sort(nums, start, split - 1)
        quick_sort(nums, split + 1, end)

# Cycle through sorting algorithms
def cycle():
    global sortpoint
    global sort
    sortlist = ['merge', 'bubble', 'insertion', 'quick']
    if sortpoint != len(sortlist) - 1:
        sortpoint += 1
        sort = sortlist[sortpoint]
    else:
        sortpoint = 0
        sort = sortlist[sortpoint]

# Function to handle button clicks
def button_click(pos, text_rects):
    if text_rects[0].collidepoint(pos):
        draw_grid()
    elif text_rects[1].collidepoint(pos):
        if sort == 'bubble':
            bubble_sort(l1)
        elif sort == 'merge':
            merge_sort(l1, 0, len(l1) - 1)
        elif sort == 'insertion':
            insertion_sort(l1)
        elif sort == 'quick':
            quick_sort(l1, 0, len(l1) - 1)
    elif text_rects[2].collidepoint(pos):
        cycle()

# Main loop
while run:
    surf.fill((0, 0, 0))
    
    # Draw buttons
    buttons = ["New Array", "Sort", "Cycle Sort"]
    text_rects = []
    button_width = 150
    button_height = BUTTON_HEIGHT
    for i, button in enumerate(buttons):
        button_rect = pygame.Rect(W // 4 * (i + 1) - button_width // 2, BUTTON_Y_POS, button_width, button_height)
        pygame.draw.rect(surf, (255, 255, 0), button_rect)  # Yellow button
        text = f.render(button, 1, (0, 0, 0))  # Black text
        text_rect = text.get_rect(center=button_rect.center)
        surf.blit(text, text_rect)
        text_rects.append(button_rect)
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                draw_grid()
            if event.key == pygame.K_RETURN:
                if sort == 'bubble':
                    bubble_sort(l1)
                elif sort == 'merge':
                    merge_sort(l1, 0, len(l1) - 1)
                elif sort == 'insertion':
                    insertion_sort(l1)
                elif sort == 'quick':
                    quick_sort(l1, 0, len(l1) - 1)
            if event.key == pygame.K_c:
                cycle()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_click(event.pos, text_rects)

    redrawWindow()

pygame.quit()
