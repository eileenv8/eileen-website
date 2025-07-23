import { getBlogPosts } from '../../lib/sanity'
import { urlFor } from '../../lib/sanity'
import Image from 'next/image'
import Link from 'next/link'

export default async function BlogPage() {
  const blogPosts = await getBlogPosts()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Eileen&apos;s Website</h1>
          <nav className="mt-4">
            <div className="flex space-x-8">
              <Link href="/" className="text-gray-600 hover:text-gray-900">Home</Link>
              <Link href="/blog" className="text-gray-900 hover:text-gray-600">Blog</Link>
              <Link href="/photos" className="text-gray-600 hover:text-gray-900">Photos</Link>
              <Link href="/library" className="text-gray-600 hover:text-gray-900">Library</Link>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Blog Posts</h1>
        
        {blogPosts.length > 0 ? (
          <div className="space-y-8">
            {blogPosts.map((post) => (
              <article key={post._id} className="bg-white rounded-lg shadow-md overflow-hidden">
                <div className="md:flex">
                  {post.featuredImage && (
                    <div className="md:w-1/3">
                      <div className="aspect-video md:aspect-square relative">
                        <Image
                          src={urlFor(post.featuredImage).width(400).height(300).url()}
                          alt={post.title}
                          fill
                          className="object-cover"
                        />
                      </div>
                    </div>
                  )}
                  <div className={`p-6 ${post.featuredImage ? 'md:w-2/3' : 'w-full'}`}>
                    <h2 className="text-2xl font-bold text-gray-900 mb-3">
                      <Link href={`/blog/${post.slug.current}`} className="hover:text-blue-600">
                        {post.title}
                      </Link>
                    </h2>
                    {post.excerpt && (
                      <p className="text-gray-600 mb-4 text-lg">{post.excerpt}</p>
                    )}
                    <div className="flex items-center justify-between">
                      <div className="text-sm text-gray-500">
                        <span>By {post.author}</span>
                        <span className="mx-2">•</span>
                        <span>{new Date(post.publishedAt).toLocaleDateString()}</span>
                      </div>
                      {post.tags && post.tags.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {post.tags.slice(0, 3).map((tag, index) => (
                            <span 
                              key={index}
                              className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <h2 className="text-2xl font-semibold text-gray-600 mb-4">No blog posts yet</h2>
            <p className="text-gray-500">Check back soon for new content!</p>
          </div>
        )}
      </main>
    </div>
  )
}