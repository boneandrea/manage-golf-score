export const getPrize= (par, shot)=> {
  const diff = par - shot
  if (shot === 1) return 'HOLEINONE'

  switch (diff) {
  case -3:
    return 'TB'
  case -2:
    return 'DB'
  case -1:
    return 'B'
  case 0:
    return 'par'
  case 1:
    return 'birdie'
  case 2:
    return 'eagle'
  case 3:
    return 'ALBATROSS'
  default:
    return null
  }

}
