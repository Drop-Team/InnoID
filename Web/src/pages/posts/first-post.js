import Link from 'next/link'
import Layout from '../../components/layout'

export default function FirstPost() {
  return (
    <>
      <Layout>
        <h1>First Post</h1>
        <h2>
          <Link href="/">Back to home</Link>
        </h2>
      </Layout>
    </>
  )
}