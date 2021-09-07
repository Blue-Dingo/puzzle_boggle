from copy import deepcopy


def load_map(level):
    if map_exists(level):
        return deepcopy(bubble_maps[level-1])


def map_exists(level):
    if level - 1 < len(bubble_maps):
        return True


bubble_maps = []

# bubble_maps.append(
#     [
#         list("Y......."),
#         list("Y....../"),
#         list("........"),
#         list("......./"),
#         list("........"),
#         list("......./"),
#         list("........"),
#         list("......./"),
#         list("........"),
#         list("......./"),
#         list("........")])

bubble_maps.append(
    [
        list("RRYYBBGG"),
        list("RRYYBBG/"),
        list("BBGGRRYY"),
        list("BBGGRRY/"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........")])

bubble_maps.append(
    [
        list("...YY..."),
        list("...G.../"),
        list("...R...."),
        list("...B.../"),
        list("...R...."),
        list("...G.../"),
        list("...P...."),
        list("...P.../"),
        list("........"),
        list("......./"),
        list("........")])

bubble_maps.append(
    [
        list("G......G"),
        list("RGBYRGB/"),
        list("Y......Y"),
        list("BYRGBYR/"),
        list("...R...."),
        list("...G.../"),
        list("...R...."),
        list("......./"),
        list("........"),
        list("......./"),
        list("........")])
