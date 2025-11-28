class ProductoNoEncontrado(Exception):
    pass


class StockInsuficiente(Exception):
    pass



# raise ProductoNoEncontrado() (asi para los errores)
# en vez de return 'frase de error'