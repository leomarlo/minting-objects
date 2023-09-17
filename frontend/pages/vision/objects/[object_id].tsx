import { useRouter } from 'next/router';

const ProductPage: React.FC = () => {
  const router = useRouter();
  const { object_id } = router.query;

  return (
    <div>{`hello ${object_id}`}</div>
  );
}

export default ProductPage;
