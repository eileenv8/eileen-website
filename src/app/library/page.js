import { getFileLibrary } from '../../lib/sanity'
import Link from 'next/link'

export default async function LibraryPage() {
  const files = await getFileLibrary()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Eileen&apos;s Website</h1>
          <nav className="mt-4">
            <div className="flex space-x-8">
              <Link href="/" className="text-gray-600 hover:text-gray-900">Home</Link>
              <Link href="/blog" className="text-gray-600 hover:text-gray-900">Blog</Link>
              <Link href="/photos" className="text-gray-600 hover:text-gray-900">Photos</Link>
              <Link href="/library" className="text-gray-900 hover:text-gray-600">Library</Link>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">File Library</h1>
        
        {files.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {files.map((file) => (
              <div key={file._id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                
                {/* Header with title and rating */}
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-lg font-semibold text-gray-900 flex-1 mr-2">
                    {file.title}
                  </h3>
                  {file.rating && (
                    <div className="flex-shrink-0">
                      <span className="text-yellow-500">{'⭐'.repeat(file.rating)}</span>
                    </div>
                  )}
                </div>

                {/* Author and category */}
                <div className="text-sm text-gray-600 mb-3">
                  {file.author && <span>by {file.author}</span>}
                  {file.author && file.category && <span className="mx-2">•</span>}
                  {file.category && (
                    <span className="capitalize bg-gray-100 px-2 py-1 rounded text-xs">
                      {file.category}
                    </span>
                  )}
                </div>

                {/* Description */}
                {file.description && (
                  <p className="text-gray-700 mb-4 text-sm leading-relaxed">
                    {file.description}
                  </p>
                )}

                {/* Tags */}
                {file.tags && file.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-4">
                    {file.tags.slice(0, 4).map((tag, index) => (
                      <span 
                        key={index}
                        className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}

                {/* File info and download */}
                <div className="border-t pt-4 mt-4">
                  <div className="flex items-center justify-between">
                    <div className="text-xs text-gray-500">
                      <div>Added: {new Date(file.dateAdded).toLocaleDateString()}</div>
                      {file.publicationDate && (
                        <div>Published: {new Date(file.publicationDate).toLocaleDateString()}</div>
                      )}
                    </div>
                    
                    {file.file && (
                      <a 
                        href={file.file.asset.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
                      >
                        📄 Download
                      </a>
                    )}
                  </div>
                  
                  {/* Source link */}
                  {file.sourceUrl && (
                    <div className="mt-2">
                      <a 
                        href={file.sourceUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 text-xs"
                      >
                        🔗 Original Source
                      </a>
                    </div>
                  )}
                </div>

                {/* Featured badge */}
                {file.featured && (
                  <div className="absolute top-2 right-2 bg-yellow-400 text-yellow-900 px-2 py-1 rounded-full text-xs font-semibold">
                    ⭐ Featured
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <h2 className="text-2xl font-semibold text-gray-600 mb-4">No files yet</h2>
            <p className="text-gray-500">Upload some documents in your Sanity studio!</p>
          </div>
        )}
      </main>
    </div>
  )
}