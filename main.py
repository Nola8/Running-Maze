import random
import animator
import generator
import solver
import renderer
import config

def add_bonus_cycles(probability=0.05):

    for r in range(config.R):
        for c in range(config.C - 1):
            if config.eastWall[r][c+1] == 1:  # wall still intact
                if random.random() < probability:
                    config.eastWall[r][c+1] = 0   # eat it

def main():
    animator.init()

    import pygame
    renderer.draw_grid(animator.screen)
    pygame.display.flip()
    pygame.time.delay(500)

    print('Generating maze...')
    generator.generate_maze(draw_callback=animator.generation_frame)
    print('Maze complete!')

    renderer.draw_maze(animator.screen)
    pygame.display.flip()
    pygame.time.delay(1000)   # pause so user can see the full maze

    print('Solving maze...')
    solution = solver.solve_maze(draw_callback=animator.solve_frame)

    if solution:
        print(f'Solved! Path length: {len(solution)} cells.')
        animator.show_solution(solution)
    else:
        print('No solution found (this should never happen).')

    animator.wait_for_quit()

if __name__ == '__main__':
    main()
