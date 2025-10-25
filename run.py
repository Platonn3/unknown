import heapq
import sys
from typing import Any, Generator

labyrinth_depth = 2

costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

types = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

depth_2 = {
    "A": [11, 12],
    "B": [13, 14],
    "C": [15, 16],
    "D": [17, 18]
}

depth_4 = {
    "A": [11, 12, 13, 14],
    "B": [15, 16, 17, 18],
    "C": [19, 20, 21, 22],
    "D": [23, 24, 25, 26]
}

room_4 = {
    11: "A",
    15: "B",
    19: "C",
    23: "D",
}

room_2 = {
    11: "A",
    13: "B",
    15: "C",
    17: "D",
}

depth = depth_2
rooms = room_2


def parse_data(lines: list[str]) -> str:
    global labyrinth_depth, depth, rooms
    hall = lines[1][1:12]
    depths = [lines[2][3:10:2], lines[3][1:8:2]]
    if len(lines) > 5:
        depths += [lines[4][1:8:2], lines[5][1:8:2]]

    labyrinth_depth = 2 if len(lines) == 5 else 4
    depth = depth_2 if labyrinth_depth == 2 else depth_4
    rooms = room_2 if labyrinth_depth == 2 else room_4

    positions = [x for x in hall]
    for i in range(4):
        for j in depths:
            positions.append(j[i])
    return "".join(positions)


def is_correct_room(index: int, positions: str) -> bool:
    if positions[index] == '.':
        return False
    letter = positions[index]
    return index in depth[letter]


def is_hall_path_clear(start_pos: int, end_pos: int, positions: str) -> bool:
    if start_pos < end_pos:
        for i in range(start_pos + 1, end_pos + 1):
            if positions[i] != '.':
                return False
    else:
        for i in range(end_pos, start_pos):
            if positions[i] != '.':
                return False
    return True


def get_all_ways_from_hall(positions: str) -> Generator[tuple[int, str], Any, None]:
    for i in range(11):
        if positions[i] == ".":
            continue

        letter = positions[i]
        target_room_door = types[letter]
        target_room_indices = depth[letter]


        room_is_ready = True
        for room_idx in target_room_indices:
            if positions[room_idx] != '.' and positions[room_idx] != letter:
                room_is_ready = False
                break
        if not room_is_ready:
            continue

        if not is_hall_path_clear(i, target_room_door, positions):
            continue

        final_index = -1
        for room_idx in reversed(target_room_indices):
            if positions[room_idx] == '.':
                final_index = room_idx
                break

        if final_index == -1:
            continue
        new_position = list(positions)
        new_position[i], new_position[final_index] = new_position[final_index], new_position[i]

        depth_in_room = target_room_indices.index(final_index) + 1
        steps = abs(i - target_room_door) + depth_in_room
        current_cost = steps * costs[letter]
        yield current_cost, "".join(new_position)


def get_all_ways_from_rooms(positions: str) -> Generator[tuple[int, str], Any, None]:
    room_top_indices = [11, 13, 15, 17] if labyrinth_depth == 2 else [11, 15, 19, 23]
    hall_indexes = [0, 1, 3, 5, 7, 9, 10]

    for top_cell_idx in room_top_indices:
        current_room_letter = rooms[top_cell_idx]
        current_room_door = types[current_room_letter]
        current_room_indices = depth[current_room_letter]

        for d, cell_idx in enumerate(current_room_indices):
            if positions[cell_idx] != '.':
                amphipod_letter = positions[cell_idx]

                is_in_correct_room = (amphipod_letter == current_room_letter)
                if is_in_correct_room:
                    all_below_are_correct = True
                    for subsequent_d in range(d + 1, labyrinth_depth):
                        subsequent_cell_idx = current_room_indices[subsequent_d]
                        if positions[subsequent_cell_idx] != current_room_letter:
                            all_below_are_correct = False
                            break
                    if all_below_are_correct:
                        break

                for hall_dest_idx in hall_indexes:
                    if is_hall_path_clear(current_room_door, hall_dest_idx, positions):
                        new_position = list(positions)
                        new_position[cell_idx], new_position[hall_dest_idx] = new_position[hall_dest_idx], new_position[
                            cell_idx]

                        steps = abs(hall_dest_idx - current_room_door) + (d + 1)
                        current_cost = steps * costs[amphipod_letter]
                        yield current_cost, "".join(new_position)

                break



def is_final_state(position: str) -> bool:
    if labyrinth_depth == 2:
        return position[11:13] == "AA" and position[13:15] == "BB" and position[15:17] == "CC" and position[17:19] == "DD"
    return position[11:15] == "AAAA" and position[15:19] == "BBBB" and position[19:23] == "CCCC" and position[23:27] == "DDDD"


def get_all_ways(positions: str) -> Generator[tuple[int, str], Any, None]:
    yield from get_all_ways_from_hall(positions)
    yield from get_all_ways_from_rooms(positions)


def solve(lines: list[str]) -> int:
    initial = parse_data(lines)
    dist = {initial: 0}
    pq = [(0, initial)]
    while pq:
        energy, pos = heapq.heappop(pq)
        if energy > dist.get(pos, float('inf')):
            continue
        if is_final_state(pos):
            return energy
        for cost_add, new_pos in get_all_ways(pos):
            new_energy = energy + cost_add
            if new_energy < dist.get(new_pos, float('inf')):
                dist[new_pos] = new_energy
                heapq.heappush(pq, (new_energy, new_pos))
    return -1


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
