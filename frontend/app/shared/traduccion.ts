/** El dataset viene en inglés; la audiencia (marketing, ventas, finanzas) lee en español. */
const DICCIONARIO: Record<string, string> = {
  // Productos
  Backpack: 'Mochila', Belt: 'Cinturón', Blouse: 'Blusa', Boots: 'Botas', Coat: 'Abrigo', Dress: 'Vestido',
  Gloves: 'Guantes', Handbag: 'Bolso', Hat: 'Sombrero', Hoodie: 'Sudadera', Jacket: 'Chaqueta', Jeans: 'Jeans',
  Jewelry: 'Joyería', Pants: 'Pantalón', Sandals: 'Sandalias', Scarf: 'Bufanda', Shirt: 'Camisa', Shoes: 'Zapatos',
  Shorts: 'Shorts', Skirt: 'Falda', Sneakers: 'Tenis', Socks: 'Medias', Sunglasses: 'Lentes de sol',
  Sweater: 'Suéter', 'T-shirt': 'Camiseta',
  // Categorías
  Accessories: 'Accesorios', Clothing: 'Ropa', Footwear: 'Calzado', Outerwear: 'Abrigos',
  // Colores
  Beige: 'Beige', Black: 'Negro', Blue: 'Azul', Brown: 'Café', Charcoal: 'Gris carbón', Cyan: 'Cian', Gold: 'Dorado',
  Gray: 'Gris', Green: 'Verde', Indigo: 'Índigo', Lavender: 'Lavanda', Magenta: 'Magenta', Maroon: 'Vino',
  Olive: 'Oliva', Orange: 'Naranja', Peach: 'Durazno', Pink: 'Rosado', Purple: 'Morado', Red: 'Rojo',
  Silver: 'Plateado', Teal: 'Verde azulado', Turquoise: 'Turquesa', Violet: 'Violeta', White: 'Blanco', Yellow: 'Amarillo',
  // Envíos
  '2-Day Shipping': 'Envío en 2 días', Express: 'Exprés', 'Free Shipping': 'Envío gratis',
  'Next Day Air': 'Al día siguiente', Standard: 'Estándar', 'Store Pickup': 'Retiro en tienda',
  // Temporadas, género y otros
  Spring: 'Primavera', Summer: 'Verano', Fall: 'Otoño', Winter: 'Invierno',
  Female: 'Mujer', Male: 'Hombre', true: 'Sí', false: 'No', '<=24': '24 o menos',
}

export const es = (texto: string) => DICCIONARIO[texto] ?? texto
