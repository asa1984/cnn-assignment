#let project(title: "", authors: (), body) = {
  set document(author: authors, title: title)
  set page(numbering: "1", number-align: center)
  
  set heading(numbering: "1.")
  
  set text(font: "Noto Serif CJK JP", lang: "ja")
  // show strong: set text(font: "Noto Sans CJK JP", weight: "semibold")
  show heading: set text(font: "Noto Sans CJK JP", weight: "bold")

  align(center)[
    #block(text(font:"Noto Sans CJK JP",weight:700, 1.5em, title))
  ]

  pad(
    top: 0.5em,
    bottom: 0.5em,
    x: 2em,
    grid(
      columns: (1fr,) * calc.min(3, authors.len()),
      gutter: 1em,
      ..authors.map(author => align(center, strong(author))),
    ),
  )

  set par(justify: true)
  body
}
