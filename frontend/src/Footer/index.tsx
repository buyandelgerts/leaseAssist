const Footer = () => (
    <footer className="bg-white border-t border-slate-200 py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="text-sm text-slate-500">
          © 2026 Lease Assist. All rights reserved.
        </div>
        <div className="flex space-x-6 text-sm text-slate-500">
          <a href="#" className="hover:text-slate-900">Privacy Policy</a>
          <a href="#" className="hover:text-slate-900">Terms of Service</a>
          <a href="#" className="hover:text-slate-900">Contact Support</a>
          <a href="#" className="hover:text-slate-900">Fair Housing</a>
        </div>
      </div>
    </footer>
  );

  export default Footer;