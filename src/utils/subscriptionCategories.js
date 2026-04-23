export const SUBSCRIPTION_CATEGORIES = [
  { id: 1, name: 'Entertainment' },
  { id: 2, name: 'Productivity' },
  { id: 3, name: 'Music' },
  { id: 4, name: 'Cloud Storage' },
  { id: 5, name: 'Education' },
];

export function getDefaultCategoryId() {
  return SUBSCRIPTION_CATEGORIES[0].id;
}

export function getCategoryNameById(categoryId) {
  return SUBSCRIPTION_CATEGORIES.find((category) => category.id === categoryId)?.name
    ?? SUBSCRIPTION_CATEGORIES[0].name;
}
