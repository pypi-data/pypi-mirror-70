from . import cell


class Mesh:
    def __init__(self):
        self._cells = set()
        self._edges = set()
        self._junctions = set()

    def add_cell(self, cell_pixel_value):
        self._cells.add(cell.Cell(cell_pixel_value))

    def remove_cell(self, cell_pixel_value):
        self._cells.remove(cell.Cell(cell_pixel_value))

    @property
    def number_of_cells(self):
        """ returns the number of cells in the mesh

        :return: number of cells in mesh
        :rtype: int
        """

        return len(self._cells)

    @property
    def number_of_edges(self):
        """ returns the number of edges in the mesh

        :return: number of edges in the mesh
        :rtype: int
        """

        return len(self._edges)

    @property
    def number_of_junctions(self):
        """ returns the number of junctions in the mesh

        :return: number of junctions in the mesh
        :rtype: int
        """

        return len(self._junctions)

    @property
    def number_of_triple_junctions(self):
        """ counts and outputs the number of triple junctions in the mesh

        :return number of triple junctions in mesh
        :rtype: int
        """

        count = 0
        for junction in self._junctions:
            if junction.degree == 3:
                count += 1
        return count
