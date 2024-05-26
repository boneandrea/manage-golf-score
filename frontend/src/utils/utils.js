export const HOLE=18
export const getPrize= (par, shot)=> {
  if (shot === 1) return 'HOLEINONE'
  const diff = shot - par


  switch (diff) {
  case -3:
    return "ALBATROSS"
  case -2:
    return "EAGLE"
  case -1:
    return "BIRDIE"
  case 0:
    return "PAR"
  case 1:
    return "BOGEY"
  case 2:
    return "DOUBLEBOGEY"
  case 3:
    return "TRIPLEBOGEY"
  default:
    return null
  }

}
