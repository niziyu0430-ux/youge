// Question IDs belong to their authored pack. Only the API metadata marks ties.
export function isSupplementaryQuestion(question){
  return question?.scope==='cross'&&Number.isInteger(question.order)&&question.order>=17&&question.order<=18;
}
