import { getBlogPosts, getFeaturedPhotos } from '../lib/sanity'
import { urlFor } from '../lib/sanity'
import Image from 'next/image'
import Link from 'next/link'

export default async function Home() {
  // Fetch data from Sanity
  const blogPosts = await getBlogPosts()
  const featuredPhotos = await getFeaturedPhotos()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Eileen&apos;s Website</h1>
          <nav className="mt-4">
            <div className="flex space-x-8">
              <Link href="/" className="text-gray-900 hover:text-gray-600">Home</Link>
              <Link href="/blog" className="text-gray-600 hover:text-gray-900">Blog</Link>
              <Link href="/photos" className="text-gray-600 hover:text-gray-900">Photos</Link>
              <Link href="/library" className="text-gray-600 hover:text-gray-900">Library</Link>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        
        {/* Recent Blog Posts */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Blog Posts</h2>
          {blogPosts.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {blogPosts.slice(0, 3).map((post) => (
                <article key={post._id} className="bg-white rounded-lg shadow-md overflow-hidden">
                  {post.featuredImage && (
                    <div className="aspect-video relative">
                      <Image
                        src={urlFor(post.featuredImage).width(400).height(225).url()}
                        alt={post.title}
                        fill
                        className="object-cover"
                      />
                    </div>
                  )}
                  <div className="p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      <Link href={`/blog/${post.slug.current}`} className="hover:text-blue-600">
                        {post.title}
                      </Link>
                    </h3>
                    {post.excerpt && (
                      <p className="text-gray-600 mb-3">{post.excerpt}</p>
                    )}
                    <div className="text-sm text-gray-500">
                      {new Date(post.publishedAt).toLocaleDateString()}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <p className="text-gray-600">No blog posts yet. Create some in your Sanity studio!</p>
          )}
        </section>

        {/* Featured Photos */}
        {featuredPhotos.length > 0 && (
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Featured Photos</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              {featuredPhotos.slice(0, 4).map((photo) => (
                <div key={photo._id} className="bg-white rounded-lg shadow-md overflow-hidden">
                  <div className="aspect-square relative">
                    <Image
                      src={urlFor(photo.image).width(300).height(300).url()}
                      alt={photo.title || 'Photo'}
                      fill
                      className="object-cover"
                    />
                  </div>
                  {(photo.title || photo.location) && (
                    <div className="p-3">
                      {photo.title && (
                        <h3 className="font-medium text-gray-900">{photo.title}</h3>
                      )}
                      {photo.location && (
                        <p className="text-sm text-gray-600">{photo.location}</p>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

      </main>
    </div>
  )
}