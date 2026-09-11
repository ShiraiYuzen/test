#!/usr/bin/env python3
import pygame
import random
import math
import sys


def generate_heart_mask(cols, rows):
	mask = [[False] * rows for _ in range(cols)]
	for i in range(cols):
		for j in range(rows):
			x = (i - cols / 2) / (cols / 2) * 1.5
			y = (rows / 2 - j) / (rows / 2) * 1.5
			f = (x * x + y * y - 1) ** 3 - x * x * y * y * y
			if f <= 0:
				mask[i][j] = True
	return mask


def main():
	pygame.init()
	width, height = 900, 600
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Love Matrix - 按 Esc 退出")
	clock = pygame.time.Clock()

	font_size = 18
	# 调整为更小字体以增加密度
	# 更小字体以提高密度
	# 调整为不那么密集：增大字体以减少列数
	font_size = 14
	try:
		font = pygame.font.SysFont("Consolas", font_size, bold=True)
	except Exception:
		font = pygame.font.SysFont(None, font_size, bold=True)

	cols = width // font_size
	rows = height // font_size


	# characters for matrix-like effect
	chars = list("01ｱｲｳｴｵｶｷｸｹｺABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789♥♡")
	# use floats so we can slow down by fractional rows per frame
	drops = [float(random.randint(-rows, 0)) for _ in range(cols)]
	# make all columns drop; reduce speed by ~2x (use 0.5 rows/frame)
	speeds = [0.5 for _ in range(cols)]

	heart_mask = generate_heart_mask(cols, rows)

	# colors and background
	bg = (0, 0, 0)
	matrix_head = (180, 255, 180)
	matrix_tail_base = (0, 180, 0)
	pink = (255, 105, 180)

	# trail length for each column（不那么密集时使用中等尾迹）
	trail_len = 14

	# large font for central message inside the heart
	try:
		font_large = pygame.font.SysFont("Microsoft YaHei", int(font_size * 3), bold=True)
	except Exception:
		font_large = pygame.font.SysFont(None, int(font_size * 3), bold=True)

	# prepare text mask so the characters form the message using data-stream
	msg = "喜欢你"
	text_surf = font_large.render(msg, True, (255, 255, 255))
	text_rect = text_surf.get_rect(center=(width // 2, height // 2))
	# convert for pixel access
	text_surf = text_surf.convert_alpha()

	text_mask = [[False] * rows for _ in range(cols)]
	for i in range(cols):
		for j in range(rows):
			# sample center of cell
			px = i * font_size + font_size // 2
			py = j * font_size + font_size // 2
			tx = px - text_rect.left
			ty = py - text_rect.top
			if 0 <= tx < text_surf.get_width() and 0 <= ty < text_surf.get_height():
				c = text_surf.get_at((int(tx), int(ty)))
				# check alpha or brightness
				if (len(c) >= 4 and c[3] > 10) or (c[0] + c[1] + c[2] > 30):
					text_mask[i][j] = True

	# surface for subtle fade (creates trailing effect)
	fade_surf = pygame.Surface((width, height))
	fade_surf.set_alpha(60)
	fade_surf.fill((0, 0, 0))

	# helper to ensure valid RGB tuples
	def clamp_color(c):
		return (max(0, min(255, int(c[0]))), max(0, min(255, int(c[1]))), max(0, min(255, int(c[2]))))

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False

		screen.fill(bg)
		screen.blit(fade_surf, (0, 0))

		# draw columns with trailing characters (matrix data stream style)
		for i in range(cols):
			y = drops[i]
			x_px = i * font_size

			# draw trail from head backwards
			for t in range(trail_len):
				# compute integer row index for mask lookup and y position
				row_idx = int((y - t) % rows)
				y_px = row_idx * font_size
				ch = random.choice(chars) if t != 0 else random.choice(chars)

				# text area uses data-stream characters (highest priority), then heart highlight, else green gradient
				if text_mask[i][row_idx]:
					# emphasize text with brighter pink; vary slightly by t for depth
					intensity = 255 - min(200, t * 10)
					color = (min(255, pink[0] + int((trail_len - t) * 2)),
						max(0, pink[1] - int(t * 2)),
						min(255, pink[2] + int((trail_len - t))))
					color = clamp_color(color)
				elif heart_mask[i][row_idx]:
					# make the head brighter pink
					intensity = 255 - min(200, t * 20)
					color = (min(255, pink[0] + t * 2), max(0, pink[1] - t * 3), min(255, pink[2] + t))
					color = clamp_color(color)
				else:
					# head bright, tail darker (green)
					fade = max(20, 255 - t * (255 // trail_len))
					color = (matrix_tail_base[0] * fade // 255 + (matrix_head[0] if t == 0 else 0),
						 matrix_tail_base[1] * fade // 255 + (matrix_head[1] if t == 0 else 0),
						 matrix_tail_base[2] * fade // 255 + (matrix_head[2] if t == 0 else 0))
					color = clamp_color(color)

				surf = font.render(ch, True, color)
				# only blit if inside screen vertically
				if 0 <= y_px < height:
					screen.blit(surf, (x_px, y_px))

			drops[i] += speeds[i]
			# random reset once past bottom
			if drops[i] * font_size > height + random.randint(0, rows * font_size):
				drops[i] = float(random.randint(-rows, 0))
				speeds[i] = 0.5


		# overlay: force characters at text mask positions so the message is formed by data-stream
		for i in range(cols):
			for j in range(rows):
				if text_mask[i][j]:
					x_px = i * font_size
					y_px = j * font_size
					ch = random.choice(chars)
					# choose bright pink for text
					color = clamp_color((255, 30, 160))
					surf = font.render(ch, True, color)
					screen.blit(surf, (x_px, y_px))

		pygame.display.flip()
		# 保持高帧率以保证平滑（但画面不再那么密集）
		clock.tick(120)

	pygame.quit()


if __name__ == '__main__':
	main()

